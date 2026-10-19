"""Read-only checks of station source files against the reviewed baseline."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', help='Station source root; defaults to manifest root')
    parser.add_argument('--topic', help='Filter entries by topic, e.g. navigation or radar')
    parser.add_argument('--check', action='store_true', help='Print summary and differences only')
    args = parser.parse_args()
    manifest_path = Path(__file__).resolve().parents[1] / 'references' / 'source-index.json'
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        root = Path(args.root or manifest['root']).resolve()
        entries = [e for e in manifest['files'] if not args.topic or args.topic in e['topics']]
        if not entries:
            parser.error('No entries for this topic')
        results = []
        for entry in entries:
            path = (root / entry['path']).resolve()
            path.relative_to(root)
            result = {'path': str(path), 'status': 'missing', 'anchors': {}}
            if path.is_file():
                data = path.read_bytes()
                result['sha256'] = hashlib.sha256(data).hexdigest()
                result['status'] = 'unchanged' if result['sha256'] == entry['sha256'] else 'changed'
                lines = data.decode('utf-8-sig').splitlines()
                result['anchors'] = {
                    anchor: [i for i, line in enumerate(lines, 1) if anchor in line]
                    for anchor in entry['anchors']
                }
                if any(not hits for hits in result['anchors'].values()):
                    result['status'] = 'anchor-missing'
            results.append(result)
        differences = [r for r in results if r['status'] != 'unchanged']
        report = {
            'root': str(root), 'baseline_date': manifest['reviewed_on'],
            'checked': len(results), 'differences': len(differences),
            'files': differences if args.check else results,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if differences else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Source check failed: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
