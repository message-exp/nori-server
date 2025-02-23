#!/bin/sh

set -e

COMMIT=${1:-"origin/main"}

echo ">>> 初始化 Git Submodule"
git submodule update --init --recursive

echo ">>> 切換到指定 commit: $COMMIT"
cd ./src/protos
git fetch origin
git checkout "$COMMIT"
cd -

echo ">>> 啟動 Docker Compose"
docker compose up -d

echo ">>> 執行 alembic migrate"
docker exec -it nori-server /bin/sh -c "cd src && poetry run alembic upgrade head"


