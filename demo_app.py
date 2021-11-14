import streamlit as st
from find_search_tags import FindSearchTags

st.title('Поисковые подсказки Демо')

st.markdown('**Демо стэнд**')




with st.form('form'):
	text_input = st.text_area('Введите запрос сюда: ', '...')
	submit_button = st.form_submit_button('Поиск')

	if submit_button:
		fsg = FindSearchTags()
		output = fsg.find_related_products(text_input)
		st.write(output)
