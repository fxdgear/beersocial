# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Beer.type'
        db.add_column('beers_beer', 'type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['beers.BeerType'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field type on 'Beer'
        db.delete_table('beers_beer_type')


    def backwards(self, orm):
        
        # Deleting field 'Beer.type'
        db.delete_column('beers_beer', 'type_id')

        # Adding M2M table for field type on 'Beer'
        db.create_table('beers_beer_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('beer', models.ForeignKey(orm['beers.beer'], null=False)),
            ('beertype', models.ForeignKey(orm['beers.beertype'], null=False))
        ))
        db.create_unique('beers_beer_type', ['beer_id', 'beertype_id'])


    models = {
        'beers.beer': {
            'Meta': {'object_name': 'Beer'},
            'brewery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['beers.Brewery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['beers.BeerType']", 'null': 'True', 'blank': 'True'})
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
