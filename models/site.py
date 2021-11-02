from sql_alchemy import banco

class SiteModel(banco.Model):
	__tablename__= 'sites'

	site_id = banco.Column(banco.Integer, primary_key=True)
	url = banco.Column(banco.String(80))
	hoteis = banco.relationship('HotelModel') # Lista de objectos hoteis
	
	def __init__(self,url):
		self.url=url


	def json(self):
		return {
		'site_id':self.site_id,
		'url':self.url,
		'hoteis':[hotel.json() for hotel in self.hoteis]
		}

	@classmethod
	def find_site(cls, url):
		
		site= cls.query.filter_by(url=url).first() #Select * from sites where site_id=**site_id
		if site:
			return site
		return None


	@classmethod
	def find_by_id(cls, site_id):
		
		site= cls.query.filter_by(site_id=site_id).first() #Select * from sites where site_id=**site_id
		if site:
			return site
		return None



	def save_site(self):
		banco.session.add(self)
		banco.session.commit()

	
	def delete_site(self):

		[hotel.delete_hotel() for hotel in self.hoteis] # deleta todos os hoteis
		banco.session.delete(self) # delete select * from sites where hotel_id=**hotel_id
		# sera que no funciona banco.session.delete(self.hoteis)
		banco.session.commit()