**Blog implementation just for fun**
*is a project with more education purposes than actual needs*
...But it has even API and test coverage!

Things that had been made:
- API (CRUD support, serialization) with 100% test coverage
- templates (for the ~half of urls, but it is better than nothing)) 
- admin panel in blog
- queries optimization (caching fields, annotates and aggregates, joins using select_ and prefetch_related)
- a humble attempt of celery integration together with redis as a message broker
- and yep, email sending tasks (google smtp)
- OAuth 2.0 github integration
- mostly Class Based Views
- 1 signal receiving case (in test...)
- custom permissions
