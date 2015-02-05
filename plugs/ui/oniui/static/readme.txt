This directory is used to store static files.

How to integrate avalon.oniui static files:
    Use this cmd to modify {{}} to {%%}
        find .|grep \.html|xargs perl -pi -e 's|{{|{%|g'
        find .|grep \.html|xargs perl -pi -e 's|}}|%}|g'
    Then modify oniui-common.css
        from "http://simg4.qunarzz.com/fonts/fontawesome/4.2.0/" to "/static/fontawesome/4.2.0/fonts/"
    Modify loading/avalon.loading.js
        from "https://source.qunarzz.com/piao/images/loading_camel.gif" to "./loading_camel.gif"
