# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Card'
        db.create_table('valentunes_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('recipient_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('recipient_email', self.gf('django.db.models.fields.EmailField')(max_length=200, blank=True)),
            ('recipient_phone', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('intro_note', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('interests', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('valentunes', ['Card'])

        # Adding model 'Track'
        db.create_table('valentunes_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('track_mbid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('track_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('album_coverart_100x100', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('artist_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('artist_mbid', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('audio_url', self.gf('django.db.models.fields.URLField')(max_length=640)),
            ('search_term', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('remove', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('valentunes', ['Track'])

        # Adding M2M table for field card on 'Track'
        db.create_table('valentunes_track_card', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm['valentunes.track'], null=False)),
            ('card', models.ForeignKey(orm['valentunes.card'], null=False))
        ))
        db.create_unique('valentunes_track_card', ['track_id', 'card_id'])

        # Adding model 'UserProfile'
        db.create_table('valentunes_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('valentunes', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Card'
        db.delete_table('valentunes_card')

        # Deleting model 'Track'
        db.delete_table('valentunes_track')

        # Removing M2M table for field card on 'Track'
        db.delete_table('valentunes_track_card')

        # Deleting model 'UserProfile'
        db.delete_table('valentunes_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'valentunes.card': {
            'Meta': {'object_name': 'Card'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'intro_note': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'recipient_email': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'blank': 'True'}),
            'recipient_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'recipient_phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'valentunes.track': {
            'Meta': {'object_name': 'Track'},
            'album_coverart_100x100': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'artist_mbid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'artist_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'audio_url': ('django.db.models.fields.URLField', [], {'max_length': '640'}),
            'card': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'track_card_set'", 'symmetrical': 'False', 'to': "orm['valentunes.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remove': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'track_mbid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'track_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'valentunes.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['valentunes']
