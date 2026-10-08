#!/usr/bin/env python3
"""Search the local book index; no network access, uploads or modifications."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYWORDS = ('担保', '通勤', '续费', '工伤', '夜班', '失业', '医保', '预售', '出生医学证明',
            '监护', '留学', '基金', '房贷', '低钠盐', '血压', '借款', '欺凌', '爬虫',
            '手机丢', '卧床', '死亡证明', '继承', '签证', '退役', '培训', '骨折')
CONCEPTS = {'实施意图': ('4.1',), '沉没成本': ('4.3',), '退出条件': ('4.2',),
            '参考类预测': ('4.4',), '检索练习': ('23.14', '23.19'),
            '间隔练习': ('23.15',), '交错练习': ('23.17',), '退款': ('5.22', '5.29'),
            '五笔账': ('10.9', '10.10', '10.15', '10.16', '10.17')}

def normalized(text):
    return re.sub(r'[^\w]', '', unicodedata.normalize('NFKC', text).lower())

def search(query='', entry_id=None, chapter=None, evidence=None, limit=8):
    records = json.loads((ROOT / 'references/entry-index.json').read_text(encoding='utf-8'))
    query = normalized(query)
    if not query and not any([entry_id, chapter, evidence]):
        raise ValueError('请提供关键词、--id、--chapter或--evidence。')
    ranked = []
    important_words = [word for word in KEYWORDS if word in query]
    for record in records:
        if entry_id and record['id'] != entry_id:
            continue
        if chapter and record['chapter'] != chapter:
            continue
        if evidence and record['evidence_in_book'] != evidence:
            continue
        title = normalized(record['title'])
        score = 0
        if query:
            concept_match = any(concept in query and record['id'] in ids for concept, ids in CONCEPTS.items())
            if important_words and not any(word in title for word in important_words) and not concept_match:
                continue
            if query in title:
                score = 100 + min(len(query), 20)
            else:
                pairs = {query[i:i+2] for i in range(len(query)-1)}
                score = sum(2 for pair in pairs if pair in title)
            score += sum(30 for word in important_words if word in title)
            score += sum(100 for concept, ids in CONCEPTS.items() if concept in query and record['id'] in ids)
            if not score:
                continue
        ranked.append((score, record))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]['chapter'], pair[1]['entry']))
    return [record for _, record in ranked[:limit]]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--id', dest='entry_id')
    parser.add_argument('--chapter', type=int, choices=range(1, 34))
    parser.add_argument('--evidence', choices=['A', 'B', 'C'])
    parser.add_argument('--limit', type=int, default=8)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('--limit必须为正整数。')
    try:
        result = search(args.query, args.entry_id, args.chapter, args.evidence, args.limit)
    except ValueError as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not result:
        print('未找到匹配条目；请换关键词或按章节查询。')
    else:
        for item in result:
            pages = item['pdf_pages']
            span = str(pages[0]) if pages[0] == pages[1] else f'{pages[0]}–{pages[1]}'
            print(f"{item['id']}  {item['title']}")
            print(f"  书中证据 {item['evidence_in_book']}；PDF页 {span}；{item['chapter_file']}")
            print('  标记：' + ('；'.join(item['flags']) or '未检出争议／待核实字样，不代表已经核验'))
            print('  来源片段：' + item['bibliography_hint'])
        print('\n标题用于定位；具体操作、数字和现行政策须回读及核验。')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
