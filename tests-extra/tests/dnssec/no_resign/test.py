#!/usr/bin/env python3

'''Test for no resigning if the zone is properly signed.'''

from dnstest.utils import *
from dnstest.test import Test
import dns

# Changes in NSEC allowed due to case changes (Knot lowercases all owners).
def only_nsec_changed(server, zone, serial):
   resp = master.dig(nsec_zone, "IXFR", serial=serial)
   for msg in resp.resp:                                                   
       for rr in msg.answer:
            if rr.rdtype not in [dns.rdatatype.SOA, dns.rdatatype.NSEC, dns.rdatatype.RRSIG]:
                return False
            if rr.rdtype == dns.rdatatype.RRSIG:
                if (not rr.match(rr.name, rr.rdclass, dns.rdatatype.RRSIG, dns.rdatatype.NSEC)) and \
                   (not rr.match(rr.name, rr.rdclass, dns.rdatatype.RRSIG, dns.rdatatype.SOA)):
                    # RRSIG covering something else than NSEC or SOA.
                    return False
   return True

t = Test()

master = t.server("knot")
nsec_zone = t.zone_rnd(1, dnssec=True, nsec3=False)
nsec3_zone = t.zone_rnd(1, dnssec=True, nsec3=True)
static_zone = t.zone("example.", storage=".")
t.link(nsec_zone, master)
t.link(nsec3_zone, master)
t.link(static_zone, master)

t.start()

# Get zone serial.
old_nsec_serial = master.zone_wait(nsec_zone)
old_nsec3_serial = master.zone_wait(nsec3_zone)
old_static_serial = master.zone_wait(static_zone)

# Enable autosigning.
master.dnssec_enable = True
master.use_keys(nsec_zone)
master.use_keys(nsec3_zone)
master.use_keys(static_zone)
master.gen_confile()
t.sleep(1)
master.stop()
master.start()

new_nsec_serial = master.zone_wait(nsec_zone)
new_nsec3_serial = master.zone_wait(nsec3_zone)
new_static_serial = master.zone_wait(static_zone)

# Check if the zones are resigned.
if old_nsec_serial < new_nsec_serial:
    if not only_nsec_changed(master, nsec_zone, old_nsec_serial):
        set_err("NSEC zone got resigned")
    old_nsec_serial = new_nsec_serial

compare(old_nsec3_serial, new_nsec3_serial, "NSEC3 zone got resigned")
compare(old_static_serial, new_static_serial, "static zone got resigned")

t.stop()
