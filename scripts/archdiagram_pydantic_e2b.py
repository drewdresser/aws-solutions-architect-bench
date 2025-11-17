from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModelSettings
from pydantic import BaseModel
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox  # type: ignore
import base64
import re
import logging
from pathlib import Path

# Set up logging - only show warnings and errors
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
# Override logger level to show success messages
logger.setLevel(logging.INFO)

load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# Architecture diagram prompt - customize this to generate different diagrams
ARCHITECTURE_PROMPT = (
    "Your job is to return an image of the architecture diagram. "
    "To do that you should use python diagrams library to generate the diagram. "
    "Then you should run the code to generate the image. "
    "If any packages or system dependencies are missing, install them using the run_shell_command tool first. "
    "Build a diagram of a three tier architecture on AWS with Amplify, API Gateway and Lambda and DynamoDB."
)

# Model settings for OpenAI with code execution outputs
model_settings = OpenAIResponsesModelSettings(
    openai_include_code_execution_outputs=True
)

# Create the agent with a custom E2B code execution tool
agent = Agent[None, str](
    "openai-responses:gpt-5.1",
    model_settings=model_settings,
    system_prompt="You are an expert at creating AWS architecture diagrams using Python's diagrams library. "
    "You can execute Python code using the E2B code interpreter to generate diagrams. "
    "If you encounter missing packages or dependencies, first use check_environment to understand what's available, "
    "then use run_shell_command to install them. "
    "For Python packages: 'pip install diagrams' "
    "For system packages: The E2B code interpreter sandbox may have restrictions. Try 'sudo apt-get install -y graphviz' "
    "but if that fails due to permissions, you may need to work around it or use alternative approaches. "
    "Always check the environment first to understand what package managers and permissions are available.",
)


class CodeExecutionResult(BaseModel):
    """Result of code execution."""

    success: bool
    output: str
    error: str | None = None
    files: list[str] = []


# Store the sandbox instance
_sandbox: Sandbox | None = None


def get_sandbox() -> Sandbox:
    """Get or create the E2B sandbox instance."""
    global _sandbox
    if _sandbox is None:
        _sandbox = Sandbox.create()
    return _sandbox


@agent.tool
def check_environment(ctx: RunContext[None]) -> CodeExecutionResult:
    """
    Check the E2B sandbox environment to understand what's available.

    This tool helps identify:
    - What package manager is available (apt-get, yum, dnf, etc.)
    - What user we're running as (root or regular user)
    - What's already installed
    - System information

    Returns:
        Result containing environment information
    """
    try:
        sandbox = get_sandbox()

        # Check multiple things in parallel
        checks = [
            ("whoami", "Current user"),
            ("id", "User ID and groups"),
            ("which apt-get", "apt-get availability"),
            ("which yum", "yum availability"),
            ("which dnf", "dnf availability"),
            ("which pip", "pip availability"),
            ("which python3", "python3 availability"),
            ("which dot", "graphviz dot availability"),
            ("cat /etc/os-release", "OS information"),
        ]

        output_parts: list[str] = []
        output_parts.append("Environment Check Results:")
        output_parts.append("=" * 50)

        for cmd, description in checks:
            try:
                result = sandbox.commands.run(cmd, timeout=10)
                status = "✓" if result.exit_code == 0 else "✗"
                output_parts.append(f"\n{status} {description}:")
                if result.stdout:
                    output_parts.append(f"  {result.stdout.strip()}")
                if result.stderr and result.exit_code != 0:
                    output_parts.append("  (not found)")
            except Exception as e:
                output_parts.append(f"\n✗ {description}: Error - {str(e)}")

        output = "\n".join(output_parts)

        return CodeExecutionResult(
            success=True,
            output=output,
            files=[],
        )

    except Exception as e:
        return CodeExecutionResult(
            success=False,
            output="",
            error=f"Environment check error: {str(e)}",
            files=[],
        )


@agent.tool
def run_shell_command(ctx: RunContext[None], command: str) -> CodeExecutionResult:
    """
    Run a shell command in the E2B sandbox environment.

    This tool allows you to install packages, run system commands, or perform
    any shell operations needed to set up the environment.

    IMPORTANT: If you need to install system packages and get permission errors:
    - Try with sudo: "sudo apt-get update && sudo apt-get install -y graphviz"
    - Or check the environment first using check_environment tool to see what's available
    - The E2B code interpreter sandbox may have restrictions on system package installation

    Examples:
    - Install Python packages: "pip install diagrams"
    - Install system packages (try with sudo): "sudo apt-get update && sudo apt-get install -y graphviz"
    - Check if something is installed: "which python3"
    - Run any shell command: "ls -la"

    Args:
        command: Shell command to execute

    Returns:
        Result containing command output, exit code, and any errors
    """
    try:
        sandbox = get_sandbox()

        # Run the shell command
        result = sandbox.commands.run(
            command, timeout=120
        )  # 2 minute timeout for installs

        # Collect output
        output_parts: list[str] = []

        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")

        output = "\n".join(output_parts) if output_parts else "Command executed"

        # Check exit code
        if result.exit_code != 0:
            return CodeExecutionResult(
                success=False,
                output=output,
                error=f"Command exited with code {result.exit_code}",
                files=[],
            )

        return CodeExecutionResult(
            success=True,
            output=output,
            files=[],
        )

    except Exception as e:
        return CodeExecutionResult(
            success=False,
            output="",
            error=f"Command execution error: {str(e)}",
            files=[],
        )


@agent.tool
def list_files(ctx: RunContext[None], directory: str = ".") -> CodeExecutionResult:
    """
    List files in a directory in the E2B sandbox.

    This tool helps you find generated files like diagram images.

    Args:
        directory: Directory path to list (default: current directory ".")

    Returns:
        Result containing the list of files and directories
    """
    try:
        sandbox = get_sandbox()

        # Use ls command to list files
        result = sandbox.commands.run(f"ls -lah {directory}", timeout=10)

        output_parts: list[str] = []
        output_parts.append(f"Files in {directory}:")
        output_parts.append("=" * 50)

        if result.stdout:
            output_parts.append(result.stdout)
        if result.stderr:
            output_parts.append(f"\nSTDERR:\n{result.stderr}")

        output = "\n".join(output_parts)

        if result.exit_code != 0:
            return CodeExecutionResult(
                success=False,
                output=output,
                error=f"Command exited with code {result.exit_code}",
                files=[],
            )

        return CodeExecutionResult(
            success=True,
            output=output,
            files=[],
        )

    except Exception as e:
        return CodeExecutionResult(
            success=False,
            output="",
            error=f"File listing error: {str(e)}",
            files=[],
        )


@agent.tool
def execute_python_code(ctx: RunContext[None], code: str) -> CodeExecutionResult:
    """
    Execute Python code using E2B code interpreter.

    This tool can execute Python code in a sandboxed environment. It's particularly
    useful for generating architecture diagrams using the diagrams library.

    If you encounter import errors or missing packages, use the run_shell_command
    tool first to install the required packages (e.g., "pip install diagrams").

    Args:
        code: Python code to execute

    Returns:
        Result containing execution output, any errors, and generated files
    """
    try:
        sandbox = get_sandbox()

        # Execute the code - E2B sandbox.run_code() returns an Execution object
        execution = sandbox.run_code(code)

        # Check for errors first
        if execution.error:
            error_msg = f"{execution.error.name}: {execution.error.value}\n{execution.error.traceback}"
            return CodeExecutionResult(
                success=False,
                output="",
                error=error_msg,
                files=[],
            )

        # Collect output from results
        output_parts: list[str] = []
        files: list[str] = []
        image_data: bytes | None = None
        image_filename: str | None = None

        # Process each result in the execution
        for result in execution.results:
            # Handle text output
            if result.text:
                output_parts.append(result.text)

            # Handle image output (PNG, JPEG, SVG) - these contain base64 encoded data
            if result.png:
                try:
                    # PNG data is base64 encoded in E2B
                    image_data = base64.b64decode(result.png)
                    image_filename = "diagram.png"
                    output_parts.append("PNG image generated successfully")
                except Exception as e:
                    logger.error(f"Failed to decode PNG data: {str(e)}")
                    output_parts.append(
                        f"PNG image generated but decode error: {str(e)}"
                    )
            if result.jpeg:
                try:
                    image_data = base64.b64decode(result.jpeg)
                    image_filename = "diagram.jpeg"
                    output_parts.append("JPEG image generated successfully")
                except Exception as e:
                    logger.error(f"Failed to decode JPEG data: {str(e)}")
                    output_parts.append(
                        f"JPEG image generated but decode error: {str(e)}"
                    )
            if result.svg:
                # SVG is typically text, not base64
                if result.svg:
                    svg_bytes = result.svg.encode("utf-8")
                    image_data = svg_bytes
                    image_filename = "diagram.svg"
                    output_parts.append("SVG image generated successfully")

            # Handle HTML output
            if result.html:
                output_parts.append("HTML output generated")

            # Handle markdown output
            if result.markdown:
                output_parts.append(result.markdown)

        # Also check execution.text property for main result
        if execution.text and execution.text not in output_parts:
            output_parts.insert(0, execution.text)

        # Check if output mentions a file path and try to read it from the sandbox
        output_text = "\n".join(output_parts) if output_parts else ""

        # Try multiple patterns to find file references
        file_path_match = re.search(
            r"sandbox:([^\s\)]+\.(png|jpg|jpeg|svg))", output_text, re.IGNORECASE
        )
        filename_match = re.search(
            r"[`'\"]([^\s`'\"]+\.(png|jpg|jpeg|svg))[`'\"]", output_text, re.IGNORECASE
        )
        simple_filename_match = re.search(
            r"\b([a-zA-Z0-9_-]+\.(png|jpg|jpeg|svg))\b", output_text, re.IGNORECASE
        )

        # Determine which path to use
        sandbox_path = None
        if file_path_match:
            sandbox_path = file_path_match.group(1)
        elif filename_match:
            sandbox_path = filename_match.group(1)
        elif simple_filename_match:
            sandbox_path = simple_filename_match.group(1)

        if sandbox_path and not image_data:
            try:
                # Try to read the file from sandbox
                file_data = sandbox.files.read(sandbox_path, format="bytes")
                if file_data and isinstance(file_data, bytearray):
                    image_data = bytes(file_data)
                    image_filename = Path(sandbox_path).name
                    output_parts.append(
                        f"Successfully retrieved image file: {sandbox_path}"
                    )
            except Exception:
                # Try common diagram output locations
                common_paths = [
                    f"/{sandbox_path}",
                    f"./{sandbox_path}",
                    sandbox_path,
                    "/architecture_diagram.png",
                    "/diagram.png",
                    "./architecture_diagram.png",
                    "./diagram.png",
                ]
                # Remove duplicates while preserving order
                seen = set()
                unique_paths = []
                for path in common_paths:
                    if path not in seen:
                        seen.add(path)
                        unique_paths.append(path)
                common_paths = unique_paths
                for common_path in common_paths:
                    try:
                        file_data = sandbox.files.read(common_path, format="bytes")
                        if file_data and isinstance(file_data, bytearray):
                            image_data = bytes(file_data)
                            image_filename = Path(common_path).name
                            output_parts.append(f"Found image at: {common_path}")
                            break
                    except Exception:
                        continue

        # Save image to local file if we have image data
        if image_data and image_filename:
            output_dir = Path("results/diagrams")
            output_dir.mkdir(parents=True, exist_ok=True)
            local_path = output_dir / image_filename
            try:
                with open(local_path, "wb") as f:
                    f.write(image_data)
                logger.info(f"✅ Saved image to: {local_path}")
                files.append(str(local_path))
                output_parts.append(f"\n✅ Image saved to: {local_path}")
            except Exception as e:
                logger.error(f"Failed to save image: {str(e)}")
                output_parts.append(f"\n❌ Failed to save image: {str(e)}")

        output = (
            "\n".join(output_parts) if output_parts else "Code executed successfully"
        )

        return CodeExecutionResult(success=True, output=output, files=files)

    except Exception as e:
        return CodeExecutionResult(
            success=False, output="", error=f"Execution error: {str(e)}", files=[]
        )


def extract_and_save_image_from_output(output_text: str) -> str | None:
    """
    Extract filename from agent output and try to read/save the image file.
    Returns the local file path if successful, None otherwise.
    """
    # Try multiple patterns to find file references
    patterns = [
        r"sandbox:([^\s\)]+\.(png|jpg|jpeg|svg))",  # sandbox: paths
        r"[`'\"]([^\s`'\"]+\.(png|jpg|jpeg|svg))[`'\"]",  # backticks/quotes
        r"\b([a-zA-Z0-9_-]+\.(png|jpg|jpeg|svg))\b",  # simple filename
    ]

    filename = None
    for pattern in patterns:
        match = re.search(pattern, output_text, re.IGNORECASE)
        if match:
            filename = match.group(1)
            break

    if not filename:
        return None

    # Try to read the file from sandbox
    sandbox = get_sandbox()
    paths_to_try = [
        filename,
        f"/{filename}",
        f"./{filename}",
        f"/home/user/{filename}",
    ]

    for path in paths_to_try:
        try:
            file_data = sandbox.files.read(path, format="bytes")
            if file_data and isinstance(file_data, bytearray):
                image_data = bytes(file_data)

                # Save to local file
                output_dir = Path("results/diagrams")
                output_dir.mkdir(parents=True, exist_ok=True)
                local_path = output_dir / filename

                with open(local_path, "wb") as f:
                    f.write(image_data)

                logger.info(f"✅ Saved image to: {local_path}")
                return str(local_path)
        except Exception:
            continue

    return None


def main():
    """Main function to run the agent."""
    try:
        result = agent.run_sync(ARCHITECTURE_PROMPT)

        print("Agent Output:")
        print(result.output)
        print("\n" + "=" * 50)
        print("Tool Calls:")
        if result.response.tool_calls:
            for tool_call in result.response.tool_calls:
                print(f"  - {tool_call.tool_name}: {tool_call.args}")
        print("=" * 50)

        # Try to extract and save image from agent output
        saved_path = extract_and_save_image_from_output(result.output)
        if saved_path:
            print(f"\n✅ Image saved to: {saved_path}")
        else:
            print("\n⚠️  Could not find or save image file")

        print("\nFull Result:")
        print(result)

    finally:
        # Clean up the sandbox
        global _sandbox
        if _sandbox is not None:
            _sandbox.kill()
            _sandbox = None


if __name__ == "__main__":
    main()
