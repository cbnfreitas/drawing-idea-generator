# BACKEND

- How to run: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- curl localhost:8000/dummy
- SECONDS=0 ; sleep 10 ; echo $SECONDS
- SECONDS=0 ; curl localhost:8000/dummy; echo $SECONDS
- SECONDS=0 ; curl localhost:8000/dummy & curl localhost:8000/dummy & curl localhost:8000/dummy; echo $SECONDS

## Requirements

- Avoid IP Block: max 1 call to Google every 10s, irrespective to public or private


## Pylance hints...

- "python.languageServer": "Pylance",
- "python.analysis.diagnosticMode": "workspace",
- "python.analysis.typeCheckingMode": "basic" (# type: ignore)
- /src
- _ all _

## TODO

- Idea! Try to partially import and redefine crud base class to bypass problem with request schema!
- Merge build_crud_by_owner and simple_crud
- Schema names as camel case
- Add service error handling on routes (example, wrong schema field 'url_id')
- Self-registering route
- Self-publishing table
- Schema automatically generated from table
- build_simple_crud signature

## Test

- `alias test_='python -m pytest --cov=app app/tests/ --cov-report=term-missing'`
- `pytest -v`
- `pytest -v -k TestName`
- `--pdb`: runs the debugger when an error is encountered
- `--lf`: runs only the tests that failed on the last attempt.
- Use mjml extension of VSCode to export to j2/hmtl
- `# type: ignore`


## References

- https://stackoverflow.com/questions/51158652/test-sqlalchemy-column-type
- https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
- https://github.com/samuelcolvin/pydantic/issues/650
- https://medium.com/analytics-vidhya/camel-case-models-with-fast-api-and-pydantic-5a8acb6c0eee
- https://github.com/samuelcolvin/pydantic/issues/1460
- https://github.com/kolypto/py-sa2schema (use it later)
- https://stackoverflow.com/questions/62765136/python-what-is-the-right-way-to-run-functions-in-asyncio
- 😄 _Installing Heroku Postgres with Flask!_: https://www.youtube.com/watch?v=FKy21FnjKS0
- 😆 _Emoji list_: https://gist.github.com/rxaviers/7360908
- 😄 _Sort imports_: https://eshlox.net/2019/12/02/vscode-sort-python-imports-automatically
- 😄 https://moz.com/ugc/geolocation-the-ultimate-tip-to-emulate-local-search
- 🐱 _Example of meme with giphy!_ https://codepen.io/ChynoDeluxe/pen/WGQzWW
- ❤️ _Search per city_ https://blog.linkody.com/seo-local/uule-2
- https://boomient.com/how-to-search-google-from-another-location
- 👎 It blocked the ip very soon... https://python-googlesearch.readthedocs.io/en/latest/
- https://www.geeksforgeeks.org/performing-google-search-using-python-code/ :-)
- 👍 https://stackoverflow.com/questions/41047795/python-beautifulsoup-parsing-speed-improvement
- https://stackoverflow.com/questions/48897586/extracting-href-from-a-beautiful-soup
- https://www.youtube.com/watch?v=RkaHdOje-cI
- 😢 Filipe Champs, GOOGLE API TUTORIAL: Custom Search e Google Images (JSON API) https://www.youtube.com/watch?v=LzPuCVhdUew&t=320s
- 😢 https://programmablesearchengine.google.com/cse/all

## Which city? &uule

Guarulhos
&uule=w+CAIQICIjR3VhcnVsaG9zLFN0YXRlIG9mIFNhbyBQYXVsbyxCcmF6aWw=&cr=BR

Guarulhos,State of Sao Paulo,Brazil

j

R3VhcnVsaG9zLFN0YXRlIG9mIFNhbyBQYXVsbyxCcmF6aWw=

BR

&uule=w+CAIQICIjR3VhcnVsaG9zLFN0YXRlIG9mIFNhbyBQYXVsbyxCcmF6aWw=&cr=BR

url = f"{GOOGLE_URL}/search?q={terms_plus}&num={MAX_RESULTS}&gl=br"

https://www.google.com.br/search?q=restaurantes&num=10&uule=w+CAIQICIjR3VhcnVsaG9zLFN0YXRlIG9mIFNhbyBQYXVsbyxCcmF6aWw=&cr=BR

Itapetininga,State of Sao Paulo,Brazil

m

SXRhcGV0aW5pbmdhLFN0YXRlIG9mIFNhbyBQYXVsbyxCcmF6aWw=

BR

&uule=w+CAIQICI + <string key> + ‘Canonical Name’ Base64 format + &cr=country<country ISO code>

https://www.google.com.br/search?q=restaurantes&num=10&uule=w+CAIQICImSXRhcGV0aW5pbmdhLFN0YXRlIG9mIFNhbyBQYXVsbyxCcmF6aWw=&cr=BR

Sao Jose dos Campos,State of Sao Paulo,Brazil

len = 45, t

U2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls

&uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls&cr=countryBR

## Which city? &uule 2.0

https://www.google.com/search?ie=UTF-8&oe=UTF-8
&hl=fr&q=restauran
t&adtest=on&ip=0.0.0.0&noj=1&nomo=1&nota=1&igu=1
&tci=g:1014221,p:30000
&glp=1&uule=w+CAIQICImU2FuIEZyYW5jaXNjbyxDYWxpZm9ybmlhLFVuaXRlZCBTdGF0ZXM

https://www.google.com/search?q=restaurant
&ie=UTF-8&oe=UTF-8
&hl=fr
&adtest=on
&ip=0.0.0.0&noj=1&nomo=1&nota=1&igu=1
&tci=g:1023191,p:30000
&glp=1&uule=w+CAIQICIfTmV3IFlvcmssTmV3IFlvcmssVW5pdGVkIFN0YXRlcw

https://www.google.com/search?q=criação+de+sites
&ie=UTF-8&oe=UTF-8&hl=pt-BR&ip=0.0.0.0&noj=1&nomo=1&nota=1&igu=1
&tci=g:1001772,p:30000&glp=1&uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls
&gl=br
&num=100

https://www.google.com/search?q=criação+de+material+promocional
&num=100

https://www.google.com/search?q=criação+de+sites
&ie=UTF-8&oe=UTF-8
uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls&cr=countryBR
&num=100

https://www.google.com/search?q=coworking
&num=100

&ie=UTF-8&oe=UTF-8&hl=pt-BR&ip=0.0.0.0&noj=1&nomo=1&nota=1&igu=1
&tci=g:1001772,p:30000&glp=1&uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls
&gl=br

Best parameters:
&gl=br&ie=UTF-8&oe=UTF-8&hl=pt-BR&ip=0.0.0.0&noj=1&nomo=1&nota=1&igu=1&tci=g:1001772,p:30000&glp=1&uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls
