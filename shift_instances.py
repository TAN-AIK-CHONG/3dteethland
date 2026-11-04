import json
from pathlib import Path

SRC_DIR = Path.home() / 'radboud_predictions_new'
DST_DIR = Path.home() / 'radboud_predictions_new_eval'
GUM_INSTANCE = -1


def shift_instances(pred):
    if min(pred['instances']) != GUM_INSTANCE:
        raise ValueError('expected gum instance -1')
    pred['instances'] = [instance + 1 for instance in pred['instances']]
    return pred


def main():
    pred_paths = sorted(SRC_DIR.glob('*.json'))
    for pred_path in pred_paths:
        pred = shift_instances(json.loads(pred_path.read_text()))
        (DST_DIR / pred_path.name).write_text(json.dumps(pred))
    print(f'shifted {len(pred_paths)} predictions into {DST_DIR}')


if __name__ == '__main__':
    main()