{% extends "company2/base.tpl" %}

{% block content %}

	{% if it.fullName !="" %}
		
	{% include "company2/item.tpl" ignore missing %}  

	{% else %}

	{% endif %}

    {% for it in leads %}
	
	{% include "company2/item.tpl" ignore missing %}  

    {% endfor %}
	
    {% for it in engs %}
	
	{% include "company2/item.tpl" ignore missing %}  
	
    {% endfor %}	
{% include "company2/add.tpl" ignore missing %}    
{% endblock %}