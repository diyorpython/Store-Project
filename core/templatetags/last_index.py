from django import template

register = template.Library()

@register.simple_tag(name='get_last_index')
def get_last_index(histories, all_histories):
    histories_list = []
    for history_item in histories:
        histories_list.append(history_item)
    
    all_histories_list = []
    for all_history_item in all_histories:
        all_histories_list.append(all_history_item)

    return all_histories_list.index(histories_list[-1]) + 1
