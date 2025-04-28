#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
filestoprompt.py

将指定文件夹中的所有指定后缀文件内容合并为一个 prompt，
包含项目结构和文件名，直接输出给 AI，
并自动剔除常见依赖或虚拟环境目录，
支持用户自定义屏蔽文件夹，以及排除/保留后缀。
"""

import os
import argparse


def build_structure(folder_path, allowed_exts, excluded_dirs):
    """
    构建项目结构树，只展示指定后缀文件和目录。
    支持排除指定的目录。
    """
    lines = []
    base_name = os.path.basename(os.path.abspath(folder_path))
    lines.append(f"{base_name}/")
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        rel_root = os.path.relpath(root, folder_path)
        level = 0 if rel_root == '.' else rel_root.count(os.sep) + 1
        indent = '  ' * level
        if rel_root != '.':
            lines.append(f"{indent}{os.path.basename(root)}/")
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if allowed_exts and ext not in allowed_exts:
                continue
            lines.append(f"{indent}  {fname}")
    return "\n".join(lines)


def generate_prompt(folder_path, allowed_exts, excluded_dirs, max_file_size=1024*1024):
    """
    合并文件夹内指定类型文件的内容为一个字符串，
    包含项目结构和每个文件名前缀。

    :param folder_path: 要扫描的文件夹路径
    :param allowed_exts: 允许的后缀名集合，为空则全部包含
    :param excluded_dirs: 要排除的目录列表
    :param max_file_size: 单个文件最大读取字节数，超过部分截断
    :return: 生成的 prompt 字符串
    """
    # 默认跳过的目录
    default_excludes = {'env', '.env', 'venv', '.venv', '__pycache__', 'site-packages'}
    excluded = set(default_excludes) | set(excluded_dirs)

    # 第一步：项目结构
    structure = build_structure(folder_path, allowed_exts, excluded)
    parts = ["项目结构：", structure]

    # 第二步：文件内容
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded]
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if allowed_exts and ext not in allowed_exts:
                continue
            path = os.path.join(root, fname)
            rel = os.path.relpath(path, folder_path)
            parts.append(f"=== 文件: {rel} ===")
            try:
                size = os.path.getsize(path)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(max_file_size)
                parts.append(content)
                if size > max_file_size:
                    parts.append("...（文件内容过大，已截断）")
            except Exception as e:
                parts.append(f"# 无法读取 {rel}：{e}")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(
        description="将文件夹内容合并为单个 prompt，输出到终端或文件，支持排除文件夹及后缀过滤"
    )
    parser.add_argument("folder", help="要转换的文件夹路径")
    parser.add_argument(
        "-o", "--output",
        help="将生成的 prompt 保存到指定文件（默认为终端输出）",
        default=None
    )
    parser.add_argument(
        "--max-size",
        help="单个文件最大读取大小（字节），默认 1MB",
        type=int,
        default=1024*1024
    )
    parser.add_argument(
        "--exclude",
        help="指定要排除的目录名称，多个用逗号分隔",
        default="",
    )
    parser.add_argument(
        "--exclude-ext",
        help="指定要排除的后缀名，多个用逗号分隔，例如 .log,.tmp",
        default="",
    )
    parser.add_argument(
        "--protect-ext",
        help="指定要保留的后缀名，仅包含这些后缀，多个用逗号分隔，例如 .py,.md",
        default="",
    )
    args = parser.parse_args()

    # 解析排除目录列表
    excluded_dirs = [d.strip() for d in args.exclude.split(',') if d.strip()]
    # 解析后缀过滤
    def normalize(ext):
        e = ext.strip().lower()
        return e if e.startswith('.') else f'.{e}'

    exclude_exts = {normalize(e) for e in args.exclude_ext.split(',') if e.strip()}
    protect_exts = {normalize(e) for e in args.protect_ext.split(',') if e.strip()}

    # 确定 allowed_exts
    if protect_exts:
        allowed_exts = set(protect_exts)
    else:
        # 默认允许的后缀
        allowed_exts = {'.py', '.md', '.ini', '.env', '.yaml'}
    # 排除指定后缀
    if exclude_exts:
        allowed_exts -= exclude_exts

    prompt = generate_prompt(
        args.folder,
        allowed_exts,
        excluded_dirs,
        max_file_size=args.max_size
    )

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"🎉 Prompt 已成功保存到 {args.output}！")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
