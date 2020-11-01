mkdir -p ~/.streamlit/

echo "\n\
[general]\n\
email = \"mbharadwaj@gmail.com\"\n\
\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml