{% extends "company1/base.tpl" %}

{% block content %}

	{% if it.fullName !="" %}
		
	{% include "company1/item.tpl" ignore missing %}  

	{% else %}

	{% endif %}

    {% for it in leads %}
	
	{% include "company1/item.tpl" ignore missing %}  

    {% endfor %}
	
    {% for it in engs %}
	
	{% include "company1/item.tpl" ignore missing %}  
	
    {% endfor %}	
{% include "company1/add.tpl" ignore missing %}    
{% endblock %}