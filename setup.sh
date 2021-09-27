mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
enableXsrfProtection=false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
