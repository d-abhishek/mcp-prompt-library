import { stdioServerAdapter } from "@aws/run-mcp-servers-with-aws-lambda";

const serverParams = {
  command: process.env.PY_CMD || "python3.13",
  args: ["-m", "server"],
  env: {
    PROMPTS_BUCKET: process.env.PROMPTS_BUCKET ?? "",
    PROMPTS_PREFIX: process.env.PROMPTS_PREFIX ?? "prompts/",
    NODE_ENV: process.env.NODE_ENV ?? "production",
  },
};

export const handler = async (event, context) => {
  return await stdioServerAdapter(serverParams, event, context);
};
