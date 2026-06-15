#!/bin/bash
# 景一知识管线 · 一键运行
# 用法: ./run.sh [scan|download|smelt|publish|all]

MODE=${1:-all}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

case $MODE in
    scan)
        python3 -c "from auto_pipeline import scan; scan()"
        ;;
    download)
        python3 -c "from auto_pipeline import download; download()"
        ;;
    smelt)
        python3 -c "from auto_pipeline import smelt; smelt()"
        ;;
    publish)
        python3 -c "from auto_pipeline import publish; publish()"
        ;;
    all)
        python3 "$SCRIPT_DIR/auto_pipeline.py"
        ;;
    *)
        echo "用法: ./run.sh [scan|download|smelt|publish|all]"
        ;;
esac
