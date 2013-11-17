# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Circle'
        db.create_table(u'addressbook_circle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'addressbook', ['Circle'])

        # Adding model 'UserInfo'
        db.create_table(u'addressbook_userinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'addressbook', ['UserInfo'])

        # Adding M2M table for field circle on 'UserInfo'
        m2m_table_name = db.shorten_name(u'addressbook_userinfo_circle')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userinfo', models.ForeignKey(orm[u'addressbook.userinfo'], null=False)),
            ('circle', models.ForeignKey(orm[u'addressbook.circle'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userinfo_id', 'circle_id'])

        # Adding model 'Contact'
        db.create_table(u'addressbook_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friend', to=orm['auth.User'])),
            ('invitation_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invitation_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('optional_informations', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['addressbook.UserInfo'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'addressbook', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'Circle'
        db.delete_table(u'addressbook_circle')

        # Deleting model 'UserInfo'
        db.delete_table(u'addressbook_userinfo')

        # Removing M2M table for field circle on 'UserInfo'
        db.delete_table(db.shorten_name(u'addressbook_userinfo_circle'))

        # Deleting model 'Contact'
        db.delete_table(u'addressbook_contact')


    models = {
        u'addressbook.circle': {
            'Meta': {'object_name': 'Circle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'addressbook.contact': {
            'Meta': {'object_name': 'Contact'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invitation_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'optional_informations': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['addressbook.UserInfo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friend'", 'to': u"orm['auth.User']"})
        },
        u'addressbook.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'circle': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['addressbook.Circle']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['addressbook']