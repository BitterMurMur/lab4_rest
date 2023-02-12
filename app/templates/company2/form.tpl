{% extends "company2/base.tpl" %}

{% block content %}
{{it.show()}}

<form action = '/company2/add' method=POST><br>
Доступные должности: Директор, Ведущий инженер, Инженер<br>
<input type=hidden name=Id value={{it.id}}><br>
<table>
<tr>
	<td>
		Имя:
	</td>
	<td>
		<input type=text name=fullName value={{it.fullName}}>
	</td>
</tr>
<tr>
	<td>
		Должность:
	</td>
	<td>	
		<input type=text name=position value={{it.position}}>
	</td>
</tr>
<tr>	
	<td>
		<input type=submit value="Добавить/изменить">
	</td>
<tr>	
</table>
</form>

{% endblock %}