import json, os, subprocess, sys

def handler(event, context):
    proc = subprocess.Popen(
        ["node", "index.mjs"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, env=os.environ.copy(),
    )
    payload = json.dumps({"event": event, "context": {"awsRequestId": getattr(context, "aws_request_id", "")}})
    out, err = proc.communicate(payload)
    if proc.returncode != 0:
        sys.stderr.write(err or "")
        raise RuntimeError(f"Adapter failed with code {proc.returncode}")
    return json.loads(out)
