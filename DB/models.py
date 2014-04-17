from django.db import models


class VPNserver(models.Model):
    ip_addr = models.IPAddressField()
    region = models.CharField(max_length = 16)
    
    def __unicode__(self):
        return self.ip_addr


class ServStats(models.Model):
    port = models.CharField(max_length = 32)
    ping = models.IntegerField(max_length = 8)
    session_count = models.IntegerField(max_length = 8)
    link_speed = models.CharField(max_length = 8)
    ping_ex = models.CharField(max_length = 8)
    update_time = models.DateTimeField(auto_now = True)
    vpn_server = models.ForeignKey(VPNserver)
    
    def __unicode__(self):
        return self.link_speed