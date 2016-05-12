## django-react

This project uses webpack to bundle all JS components (along with CSS). Once bundled, they are rendered on the server and then can be accessed through ```{{ raw rendered }}``` tag.

### Install

```
virtualenv venv
pip install -r requirements
npm install
npm run build

./manage runserver 8002
npm run react-service
```
