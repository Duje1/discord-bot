
def check_roles(msg, roles):
	if not roles:
		return True

	for role in msg.author.roles:
		if role.id in roles:
			return True

	return False

def check_scope(msg, channels, categories):
	if not channels and not categories:
		return True

	if channels and msg.channel_id in channels:
		return True

	category_id = getattr(getattr(msg, 'category', None), 'id', None)
	return categories and category_id in categories

