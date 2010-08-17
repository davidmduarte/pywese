def run(http):
	buffer = """
	<html>
		<head>
		</head>
		<body>
			%s
			%s
			<form name="login" method="post" action="?login">
				<div>
					<span>Username:</span> <input type="text" name="username" value="" />
					<span>Password:</span> <input type="password" name="password" value="" />
					<a href="javascript:document.login.submit();"><+></a>
				</div>
			</form>
		</body>
	</html>
	""" % (
		"GET: " + str(http.get()) + "<br/>",
		"POST: " + str(http.post()) + "<br/>" 
	)
	return buffer