from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
	def get(self):
		return {'site': [site.json() for site in SiteModel.query.all()] }


class Site(Resource):

	def get(self,url):
		site=SiteModel.find_site(url)
		if site:
			return site.json()
		return {'message': 'Site not found'}, 404


	def post(self,url):
		if SiteModel.find_site(url):
			return {"message": "Url '{}' already exists"}, 400, # bad request
		
		site = SiteModel(url)
		try:
			site.save_site()
		except:
			return {"message": "An internal error occurred trying to create new site"}, 500, # database saving problem
		return site.json()


	def delete(self,url):
		site = SiteModel.find_site(url)
		if site:
			try:
				site.delete_site()
				return {'message': 'Site deleted'}, 200
			except:
				return {"message": "Internal error to delete Site"}, 500, # database saving problem
		return {'message': 'Site not found'}, 404