import discord
from discord.ext import commands

class About(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name= 'about', aliases=['About', 'AboutCsi', 'AboutCSI', 'aboutCsi', 'aboutCSI'])
    async def about(self, ctx):
        await ctx.send('The Computer Science Club of INPT (CIT) is a dynamic student association at the National Institute of Posts and Telecommunications (INPT) in Morocco. Founded in 2001, CIT aims to promote computer science and information technologies within the student community.\n\nWe organize workshops, seminars, and training sessions to strengthen students\' technical skills. We also encourage the development of innovative technological projects and participate in competitions and hackathons to stimulate technical excellence.\n\nCIT plays a key role in enriching the academic experience of INPT students by preparing them for the challenges of the professional world in the field of information technologies.')
    
    @commands.command(name= 'aboutIDEH', aliases=['AboutIDEH', 'aboutideh', 'IDEH', 'ideh'])
    async def aboutIDEH(self, ctx):
        await ctx.send('**IDEH CTF** is an annual Capture The Flag competition organized by the Computer Science Club (CIT) at the National Institute of Posts and Telecommunications (INPT) in Morocco.\n\nThis event has become an **unmissable and essential** gathering for cybersecurity enthusiasts and students from across the region. Each year, IDEH CTF brings together student participants to test their skills in various cybersecurity domains including cryptography, web security, reverse engineering, forensics, and more.\n\nThe competition provides an excellent platform for students to enhance their practical cybersecurity knowledge, network with peers, and compete for recognition. IDEH CTF is not just a competition, but a celebration of cybersecurity expertise and innovation within the student community.\n\nJoin us for an unforgettable experience that combines learning, competition, and the spirit of cybersecurity!')
    

def setup(client):
    client.add_cog(About(client))