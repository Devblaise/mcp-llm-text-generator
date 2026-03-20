import sys
import os
import warnings
# Import resource and tools to register them with the MCP app
import resources
import tools    
from mcp_app import mcp

# Redirect all warnings to stderr so they don't corrupt the MCP JSON-RPC stream on stdout
warnings.showwarning = lambda msg, cat, *a, **kw: print(f"Warning: {cat.__name__}: {msg}", file=sys.stderr)

# Suppress stdout output from native libraries (e.g. sentencepiece, tokenizers)
os.environ["TOKENIZERS_PARALLELISM"] = "false"


#-------------------------
# SERVER ENTRYPOINT
#-------------------------      


if __name__ == "__main__":
    mcp.run()
