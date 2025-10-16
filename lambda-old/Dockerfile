FROM public.ecr.aws/lambda/nodejs:20 AS nodebuild
WORKDIR /opt/app
COPY lambda/package*.json ./
RUN npm ci --omit=dev || npm install --omit=dev

FROM public.ecr.aws/lambda/python:3.13
WORKDIR /var/task

# Put node in PATH (from donor)
COPY --from=nodebuild /var/lang/bin/node /usr/local/bin/node
COPY --from=nodebuild /var/lang/bin/npm  /usr/local/bin/npm
COPY --from=nodebuild /var/lang/lib/node_modules /usr/local/lib/node_modules
ENV PATH="/usr/local/bin:${PATH}" NODE_PATH="/usr/local/lib/node_modules"

# ---------- Build & install Python deps from a *clean* context ----------
# Create an isolated build dir with ONLY Python packaging files
RUN mkdir -p /opt/py
WORKDIR /opt/py
COPY pyproject.toml uv.lock ./
COPY server/ ./server/
# Build a wheel and install it (no accidental package discovery)
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
 && python -m pip wheel --no-deps --no-build-isolation -w /opt/wheels . \
 && python -m pip install --no-cache-dir /opt/wheels/*.whl

# ---------- Now copy runtime assets & Node adapter ----------
WORKDIR /var/task
# Node adapter
COPY lambda/package*.json ./
COPY --from=nodebuild /opt/app/node_modules ./node_modules
COPY lambda/index.mjs ./index.mjs
# Python shim
COPY lambda/lambda_handler.py ./lambda_handler.py
# Your runtime assets (not part of the Python package)
COPY prompts/ ./prompts/
COPY data/ ./data/
COPY README.md LICENSE ./

# (Optional) sanity check
RUN python - <<'PY'
import ssl, sys
print("Python:", sys.version)
print("OpenSSL:", ssl.OPENSSL_VERSION)
PY

CMD [ "lambda_handler.handler" ]
