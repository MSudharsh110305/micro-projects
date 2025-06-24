# Very simple keyword-based healthier alternatives
ALTERNATIVES = {
    'chocolate': ['dark chocolate (70% cocoa)', 'fruit and nut bar'],
    'soda': ['sparkling water with lemon', 'unsweetened iced tea'],
    'chips': ['baked veggie crisps', 'air-popped popcorn']
}

def suggest_alternatives(name):
    name_lower = name.lower()
    for key, opts in ALTERNATIVES.items():
        if key in name_lower:
            return opts
    return []
