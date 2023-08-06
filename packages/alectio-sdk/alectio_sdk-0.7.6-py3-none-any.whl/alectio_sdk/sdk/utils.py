from typing import Dict

def seed_comparison(best_seed_info:Dict,new_seed_info:Dict):
    return new_seed_info if new_seed_info['metric'] > best_seed_info['metric'] else best_seed_info
