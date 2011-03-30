# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Brewery'
        db.create_table('beers_brewery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('beers', ['Brewery'])

        # Adding model 'BeerType'
        db.create_table('beers_beertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('beers', ['BeerType'])

        # Adding model 'Beer'
        db.create_table('beers_beer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('brewery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['beers.Brewery'])),
        ))
        db.send_create_signal('beers', ['Beer'])

        # Adding M2M table for field type on 'Beer'
        db.create_table('beers_beer_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('beer', models.ForeignKey(orm['beers.beer'], null=False)),
            ('beertype', models.ForeignKey(orm['beers.beertype'], null=False))
        ))
        db.create_unique('beers_beer_type', ['beer_id', 'beertype_id'])


    def backwards(self, orm):
        
        # Deleting model 'Brewery'
        db.delete_table('beers_brewery')

        # Deleting model 'BeerType'
        db.delete_table('beers_beertype')

        # Deleting model 'Beer'
        db.delete_table('beers_beer')

        # Removing M2M table for field type on 'Beer'
        db.delete_table('beers_beer_type')


    models = {
        'beers.beer': {
            'Meta': {'object_name': 'Beer'},
            'brewery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['beers.Brewery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['beers.BeerType']", 'symmetrical': 'False'})
        },
        'beers.beertype': {
            'Meta': {'object_name': 'BeerType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'beers.brewery': {
            'Meta': {'object_name': 'Brewery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['beers']
