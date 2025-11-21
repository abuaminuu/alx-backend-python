from functools import functools.wraps

def transactional(func):
	"""Decorator to ensure a database transaction is committed or rolled back."""
	@functools.wrap(func)
	def wrapper(connection, *args, **kwargs):
		try:
			result = func(connection, *args, **kwargs)
			# commit for success
			connection.commit()
			return result
		except Exception as e:
			# undo transaction for failure
			connection.rollback.()
			print(f"transaction rolled back due to {e}")
			raise
	return wrapper


# function wrapped in both decorators
@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
# Example usage
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("Email updated successfully ✅")
	
