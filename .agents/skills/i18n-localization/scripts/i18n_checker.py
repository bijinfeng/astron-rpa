#!/usr/bin/env python3
"""
i18n Checker - Detects hardcoded strings and missing translations.
Scans for untranslated text in React, Vue, and Python files.
"""
import sys
import re
import json
import argparse
from pathlib import Path

# Fix Windows console encoding for Unicode output
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass  # Python < 3.7

CJK_RE = r'[\u4e00-\u9fff]'

UI_KEYS_RE = r'(title|label|placeholder|content|okText|cancelText|aria-label|alt)'

PATTERNS_UI = {
    'jsx': [
        ("toast_message", rf'\bmessage\.(success|error|warning|info)\(\s*([\'"`])[^\'"`\n]*{CJK_RE}[^\'"`\n]*\2'),
        ("ui_key_value", rf'\b{UI_KEYS_RE}\s*:\s*([\'"`])[^\'"`\n]*{CJK_RE}[^\'"`\n]*\1'),
        ("ui_attr", rf'\b{UI_KEYS_RE}\s*=\s*([\'"`])[^\'"`\n]*{CJK_RE}[^\'"`\n]*\1'),
        ("template_text", rf'>[^<]*{CJK_RE}[^<]*<'),
    ],
    'vue': [
        ("toast_message", rf'\bmessage\.(success|error|warning|info)\(\s*([\'"`])[^\'"`\n]*{CJK_RE}[^\'"`\n]*\2'),
        ("ui_key_value", rf'\b{UI_KEYS_RE}\s*:\s*([\'"`])[^\'"`\n]*{CJK_RE}[^\'"`\n]*\1'),
        ("ui_attr", rf'\b{UI_KEYS_RE}\s*=\s*([\'"`])[^\'"`\n]*{CJK_RE}[^\'"`\n]*\1'),
        ("template_text", rf'>[^<]*{CJK_RE}[^<]*<'),
    ],
    'python': [],
}

PATTERNS_ALL = {
    'jsx': PATTERNS_UI['jsx'] + [
        ("string_literal_sq", rf"'[^'\n]*{CJK_RE}[^'\n]*'"),
        ("string_literal_dq", rf'"[^"\n]*{CJK_RE}[^"\n]*"'),
        ("string_literal_tpl", rf'`[^`\n]*{CJK_RE}[^`\n]*`'),
    ],
    'vue': PATTERNS_UI['vue'] + [
        ("string_literal_sq", rf"'[^'\n]*{CJK_RE}[^'\n]*'"),
        ("string_literal_dq", rf'"[^"\n]*{CJK_RE}[^"\n]*"'),
        ("string_literal_tpl", rf'`[^`\n]*{CJK_RE}[^`\n]*`'),
    ],
    'python': [
        ("string_literal_sq", rf"'[^'\n]*{CJK_RE}[^'\n]*'"),
        ("string_literal_dq", rf'"[^"\n]*{CJK_RE}[^"\n]*"'),
    ],
}

# Patterns that indicate proper i18n usage
I18N_PATTERNS = [
    r'\$t\(',
    r'\bi18next\.t\(',
    r'\btranslate\(',
    r'\buseTranslation\b',
    r'\bt\(\s*["\']',
    r'_\(\s*["\']',
    r'\bgettext\(',
    r'\buseTranslations\b',
    r'\bFormattedMessage\b',
]

def find_locale_files(project_path: Path) -> list:
    """Find translation/locale files."""
    patterns = [
        "**/locales/**/*.json",
        "**/translations/**/*.json",
        "**/lang/**/*.json",
        "**/i18n/**/*.json",
        "**/messages/*.json",
        "**/*.po",  # gettext
    ]
    
    files = []
    for pattern in patterns:
        files.extend(project_path.glob(pattern))
    
    return [f for f in files if 'node_modules' not in str(f)]

def is_probably_locale_code(s: str) -> bool:
    return bool(re.match(r'^[a-z]{2,3}(-[A-Z]{2})?$', s))

def detect_language_and_namespace(file_path: Path) -> tuple[str, str] | tuple[None, None]:
    if file_path.suffix != '.json':
        return None, None

    stem = file_path.stem
    parent = file_path.parent.name

    if is_probably_locale_code(stem):
        return stem, 'root'

    if is_probably_locale_code(parent):
        return parent, stem

    return None, None

def check_locale_completeness(locale_files: list) -> dict:
    """Check if all locales have the same keys."""
    issues = []
    passed = []
    
    if not locale_files:
        return {'passed': [], 'issues': ["[!] No locale files found"]}
    
    locales: dict[str, dict[str, set]] = {}
    for f in locale_files:
        if f.suffix == '.json':
            try:
                lang, namespace = detect_language_and_namespace(f)
                if not lang:
                    continue
                content = json.loads(f.read_text(encoding='utf-8'))
                locales.setdefault(lang, {})
                locales[lang][namespace] = set(flatten_keys(content))
            except:
                continue
    
    if len(locales) < 2:
        passed.append(f"[OK] Found {len(locales)} language(s)")
        return {'passed': passed, 'issues': issues}
    
    passed.append(f"[OK] Found {len(locales)} language(s): {', '.join(locales.keys())}")
    
    all_langs = list(locales.keys())
    base_lang = all_langs[0]

    base_namespaces = set(locales.get(base_lang, {}).keys())
    for lang in all_langs[1:]:
        base_namespaces |= set(locales.get(lang, {}).keys())

    for namespace in sorted(base_namespaces):
        base_keys = locales[base_lang].get(namespace, set())
        
        for lang in all_langs[1:]:
            other_keys = locales.get(lang, {}).get(namespace, set())
            
            missing = base_keys - other_keys
            if missing:
                issues.append(f"[X] {lang}/{namespace}: Missing {len(missing)} keys")
            
            extra = other_keys - base_keys
            if extra:
                issues.append(f"[!] {lang}/{namespace}: {len(extra)} extra keys")
    
    if not issues:
        passed.append("[OK] All locales have matching keys")
    
    return {'passed': passed, 'issues': issues}

def flatten_keys(d, prefix=''):
    """Flatten nested dict keys."""
    keys = set()
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys.update(flatten_keys(v, new_key))
        else:
            keys.add(new_key)
    return keys

def should_skip_line(line: str) -> bool:
    return not line.strip()

def strip_inline_comment(line: str, file_type: str) -> str:
    if file_type not in ('jsx', 'vue'):
        return line
    if '//' not in line:
        return line
    idx = line.find('//')
    left = line[:idx]
    if left.count("'") % 2 == 0 and left.count('"') % 2 == 0 and left.count('`') % 2 == 0:
        return left
    return line

def is_debug_line(line: str) -> bool:
    s = line.strip()
    return s.startswith('console.') or s.startswith('logger.') or s.startswith('log.')

def compute_has_i18n(content: str) -> bool:
    return any(re.search(p, content) for p in I18N_PATTERNS)

def iter_code_files(project_path: Path, extensions: dict, ignore_tokens: list[str]) -> list[Path]:
    code_files = []
    for ext in extensions:
        code_files.extend(project_path.rglob(f"*{ext}"))
    filtered = []
    for f in code_files:
        sp = str(f)
        if any(token in sp for token in ignore_tokens):
            continue
        filtered.append(f)
    return filtered

def find_hardcoded_in_file(file_path: Path, file_type: str, patterns: list[tuple[str, str]], has_i18n: bool, include_console: bool) -> list[dict]:
    issues = []
    try:
        lines = file_path.read_text(encoding='utf-8', errors='ignore').splitlines()
    except:
        return issues
    if not patterns:
        return issues

    compiled = [(name, raw, re.compile(raw)) for name, raw in patterns]

    in_block_comment = False
    block_start = '/*' if file_type in ('jsx', 'vue') else None
    block_end = '*/' if file_type in ('jsx', 'vue') else None
    html_start = '<!--' if file_type == 'vue' else None
    html_end = '-->' if file_type == 'vue' else None

    for i, line in enumerate(lines, start=1):
        if should_skip_line(line):
            continue

        if in_block_comment:
            if block_end and block_end in line:
                in_block_comment = False
            continue

        if block_start and block_start in line and block_end and block_end not in line:
            in_block_comment = True
            continue

        if html_start and html_start in line and html_end and html_end not in line:
            in_block_comment = True
            continue

        if not include_console and is_debug_line(line):
            continue

        normalized = strip_inline_comment(line, file_type)

        for name, raw, rx in compiled:
            if rx.search(normalized):
                snippet = normalized.strip()
                if len(snippet) > 220:
                    snippet = snippet[:220] + "..."
                issues.append({
                    'file': str(file_path),
                    'line': i,
                    'snippet': snippet,
                    'pattern': raw,
                    'kind': name,
                    'has_i18n': has_i18n,
                })
                break

    return issues

def check_hardcoded_strings(project_path: Path, mode: str, include_console: bool, max_files: int | None, max_issues: int | None, ignore_tokens: list[str]) -> dict:
    """Check for hardcoded strings in code files."""
    issues_out = []
    passed = []
    
    extensions = {
        '.tsx': 'jsx', '.jsx': 'jsx', '.ts': 'jsx', '.js': 'jsx',
        '.vue': 'vue',
        '.py': 'python'
    }
    
    default_ignores = ['node_modules', '.git', 'dist', 'build', '__pycache__', 'venv']
    code_files = iter_code_files(project_path, extensions, default_ignores + ignore_tokens)
    
    if not code_files:
        return {'passed': ["[!] No code files found"], 'issues': [], 'critical_count': 0, 'hardcoded_count': 0, 'files_with_hardcoded': 0}
    
    files_with_i18n = 0
    total_hardcoded_occurrences = 0
    total_files_with_hardcoded = 0

    if max_files is not None:
        code_files = code_files[:max_files]

    output_full = False
    patterns_by_type = PATTERNS_UI if mode == 'ui' else PATTERNS_ALL

    for file_path in code_files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            ext = file_path.suffix
            file_type = extensions.get(ext, 'jsx')
            
            has_i18n = compute_has_i18n(content)
            if has_i18n:
                files_with_i18n += 1
            
            file_issues = find_hardcoded_in_file(
                file_path,
                file_type,
                patterns_by_type.get(file_type, []),
                has_i18n,
                include_console,
            )
            if file_issues:
                total_files_with_hardcoded += 1
                total_hardcoded_occurrences += len(file_issues)
                for it in file_issues:
                    if output_full:
                        continue
                    if max_issues is not None and len(issues_out) >= max_issues:
                        output_full = True
                        continue
                    issues_out.append(it)
        except:
            continue
    
    passed.append(f"[OK] Analyzed {len(code_files)} code files")
    
    if files_with_i18n > 0:
        passed.append(f"[OK] {files_with_i18n} files use i18n")
    
    issues = []
    if total_hardcoded_occurrences > 0:
        issues.append(f"[X] Found {total_hardcoded_occurrences} possible hardcoded occurrences in {total_files_with_hardcoded} files")
        for it in issues_out:
            flag = "i18n+" if it.get('has_i18n') else "i18n-"
            issues.append(f"  [X] {it['file']}:{it['line']} ({flag}) [{it.get('kind')}] {it['snippet']}")
        if output_full and max_issues is not None:
            issues.append(f"  [!] Output truncated at {max_issues} occurrences")
    else:
        passed.append("[OK] No obvious hardcoded strings detected")
    
    return {
        'passed': passed,
        'issues': issues,
        'critical_count': 1 if total_hardcoded_occurrences > 0 else 0,
        'hardcoded_count': total_hardcoded_occurrences,
        'files_with_hardcoded': total_files_with_hardcoded,
    }

def find_locale_files_with_fallback(project_path: Path, search_up: int) -> tuple[Path, list[Path]]:
    locale_files = find_locale_files(project_path)
    if locale_files:
        return project_path, locale_files
    current = project_path
    for _ in range(search_up):
        parent = current.parent
        if parent == current:
            break
        locale_files = find_locale_files(parent)
        if locale_files:
            return parent, locale_files
        current = parent
    return project_path, []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target', nargs='?', default='.')
    parser.add_argument('--mode', choices=['ui', 'all'], default='ui')
    parser.add_argument('--include-console', action='store_true')
    parser.add_argument('--max-files', type=int, default=0)
    parser.add_argument('--max-issues', type=int, default=200)
    parser.add_argument('--ignore-token', action='append', default=[])
    parser.add_argument('--locale-root', default='')
    parser.add_argument('--locale-search-up', type=int, default=6)
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()

    project_path = Path(args.target)
    max_files = None if args.max_files <= 0 else args.max_files
    max_issues = None if args.max_issues <= 0 else args.max_issues
    ignore_tokens = [t for t in args.ignore_token if t]
    
    print("\n" + "=" * 60)
    print("  i18n CHECKER - Internationalization Audit")
    print("=" * 60 + "\n")
    
    locale_root = Path(args.locale_root) if args.locale_root else project_path
    locale_base, locale_files = find_locale_files_with_fallback(locale_root, search_up=max(0, args.locale_search_up))
    locale_result = check_locale_completeness(locale_files)
    
    # Check hardcoded strings
    code_result = check_hardcoded_strings(
        project_path,
        mode=args.mode,
        include_console=args.include_console,
        max_files=max_files,
        max_issues=max_issues,
        ignore_tokens=ignore_tokens,
    )
    
    if args.format == 'json':
        payload = {
            'target': str(project_path),
            'mode': args.mode,
            'locale_search_base': str(locale_base),
            'locale': locale_result,
            'code': code_result,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        critical_issues = len([i for i in locale_result.get('issues', []) if i.startswith('[X]')]) + int(code_result.get('critical_count', 0))
        sys.exit(0 if critical_issues == 0 else 1)

    # Print results
    print("[LOCALE FILES]")
    print("-" * 40)
    if locale_files:
        print(f"  [OK] Locale search base: {locale_base}")
    for item in locale_result['passed']:
        print(f"  {item}")
    for item in locale_result['issues']:
        print(f"  {item}")
    
    print("\n[CODE ANALYSIS]")
    print("-" * 40)
    for item in code_result['passed']:
        print(f"  {item}")
    for item in code_result['issues']:
        print(f"  {item}")
    
    # Summary
    critical_issues = len([i for i in locale_result.get('issues', []) if i.startswith('[X]')]) + int(code_result.get('critical_count', 0))
    
    print("\n" + "=" * 60)
    if critical_issues == 0:
        print("[OK] i18n CHECK: PASSED")
        sys.exit(0)
    else:
        print(f"[X] i18n CHECK: {critical_issues} issues found")
        sys.exit(1)

if __name__ == "__main__":
    main()
