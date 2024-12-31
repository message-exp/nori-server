import os

proto_path = "protos"
output_dir = "src/proto_gen"
proto_target = "protos/**/*.proto"

# generate the python files from the proto files
os.system(
    "python -m grpc_tools.protoc \\\n"
    f"    --proto_path={proto_path} \\\n"
    f"    --python_out={output_dir} \\\n"
    f"    --grpc_python_out={output_dir} \\\n"
    f"    --pyi_out={output_dir} \\\n"
    f"    {proto_target}"
)

# fix the import problem in the generated files (using protoletariat)
os.system(
    "protol --create-package --in-place \\\n"
    f"    --python-out {output_dir} protoc --proto-path={proto_path} {proto_target}"
)
