from django import template

register = template.Library()

@register.simple_tag(name='get_first_index')
def get_first_index(histories, all_histories):
    histories_list = []
    for history_item in histories:
        histories_list.append(history_item)
    
    all_histories_list = []
    for all_history_item in all_histories:
        all_histories_list.append(all_history_item)

    return all_histories_list.index(histories_list[0]) + 1
