# asimtote.ios.converters.router
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



import netaddr

from ...diff import DiffConvert



# --- converter classes ---



# IP[V6] ROUTE ...



class Cvt_IPRoute(DiffConvert):
    cmd = "ip-route", None, None, None

    def _cmd(self, vrf, net, r):
        n = netaddr.IPNetwork(net)

        return ("ip route"
                + ((" vrf " + vrf) if vrf else "")
                + " " + str(n.network) + " " + str(n.netmask)
                + ((" " + r["interface"]) if "interface" in r else "")
                + ((" " + r["router"]) if "router" in r else "")
                + ((" " + str(r["metric"])) if "metric" in r else "")
                + ((" tag " + str(r["tag"])) if "tag" in r else ""))

    def remove(self, old, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, vrf, net, id):
        return self._cmd(vrf, net, new)


class Cvt_IPv6Route(DiffConvert):
    cmd = "ipv6-route", None, None, None

    def _cmd(self, vrf, net, r):
        return ("ipv6 route"
                + ((" vrf " + vrf) if vrf else "")
                + " " + net
                + ((" " + r["interface"]) if "interface" in r else "")
                + ((" " + r["router"]) if "router" in r else "")
                + ((" " + str(r["metric"])) if "metric" in r else "")
                + ((" tag " + str(r["tag"])) if "tag" in r else ""))

    def remove(self, old, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, vrf, net, id):
        return self._cmd(vrf, net, new)



# ROUTE-MAP ...



class Cvt_RtMap(DiffConvert):
    cmd = "route-map", None
    block = "rtmap-del"

    def remove(self, old, rtmap):
        return "no route-map " + rtmap


class DiffConvert_RtMap(DiffConvert):
    context = Cvt_RtMap.cmd


class Cvt_RtMap_Entry(DiffConvert_RtMap):
    cmd = None,
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return "no route-map %s %d" % (rtmap, seq)


class Cvt_RtMap_Entry_Action(DiffConvert_RtMap):
    cmd = None, "action"
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        return "route-map %s %s %d" % (rtmap, new, seq)


class DiffConvert_RtMap_Entry(DiffConvert_RtMap):
    context = DiffConvert_RtMap.context + Cvt_RtMap_Entry.cmd

    def enter(self, rtmap, rtmap_dict, seq):
        return ["route-map %s %s %d" % (rtmap, rtmap_dict["action"], seq)]


class Cvt_RtMap_MatchCmty(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "community", "communities"

class Cvt_RtMap_MatchCmty_Del(Cvt_RtMap_MatchCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for cmty in self.get_ext(rem):
            l.append(" no match community " + cmty)
        return l

class Cvt_RtMap_MatchCmty_add(Cvt_RtMap_MatchCmty):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for cmty in self.get_ext(upd):
            l.append(" match community " + cmty)
        return l


class Cvt_RtMap_MatchIPAddr(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-address"

class Cvt_RtMap_MatchIPAddr_Del(Cvt_RtMap_MatchIPAddr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for addr in self.get_ext(rem):
            l.append(" no match ip address " + addr)
        return l

class Cvt_RtMap_MatchIPAddr_Add(Cvt_RtMap_MatchIPAddr):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for addr in self.get_ext(upd):
            l.append(" match ip address " + addr)
        return l


class Cvt_RtMap_MatchIPPfxLst(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-prefix-list"

class Cvt_RtMap_MatchIPPfxLst_Del(Cvt_RtMap_MatchIPPfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for pfx in self.get_ext(rem):
            l.append(" no match ip address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPPfxLst_Add(Cvt_RtMap_MatchIPPfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for pfx in self.get_ext(upd):
            l.append(" match ip address prefix-list " + pfx)
        return l


class Cvt_RtMap_MatchIPv6Addr(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-address"

class Cvt_RtMap_MatchIPv6Addr_Del(Cvt_RtMap_MatchIPv6Addr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for addr in self.get_ext(rem):
            l.append(" no match ipv6 address " + addr)
        return l

class Cvt_RtMap_MatchIPv6Addr_Add(Cvt_RtMap_MatchIPv6Addr):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for addr in self.get_ext(upd):
            l.append(" match ipv6 address " + addr)
        return l


class Cvt_RtMap_MatchIPv6PfxLst(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-prefix-list"

class Cvt_RtMap_MatchIPv6PfxLst_Del(Cvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for pfx in self.get_ext(rem):
            l.append(" no match ipv6 address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPv6PfxLst_Add(Cvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for pfx in self.get_ext(upd):
            l.append(" match ipv6 address prefix-list " + pfx)
        return l


class Cvt_RtMap_MatchTag(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "tag"

class Cvt_RtMap_MatchTag_Del(Cvt_RtMap_MatchTag):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for tag in self.get_ext(rem):
            l.append(" no match tag " + str(tag))
        return l

class Cvt_RtMap_MatchTag_Add(Cvt_RtMap_MatchTag):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for tag in self.get_ext(upd):
            l.append(" match tag " + str(tag))
        return l


class Cvt_RtMap_SetCmty(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "community"

class Cvt_RtMap_SetCmty_Del(Cvt_RtMap_SetCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for cmty in self.get_ext(rem):
            l.append(" no set community " + cmty)
        return l

class Cvt_RtMap_SetCmty_Add(Cvt_RtMap_SetCmty):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for cmty in self.get_ext(upd):
            l.append(" set community " + cmty)
        return l


class Cvt_RtMap_SetIPNxtHop(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        vrf = None
        if "vrf" in nexthop:
            vrf = ("vrf " + nexthop["vrf"]) if nexthop["vrf"] else "global"

        return "set ip" + ((" " + vrf) if vrf else "") + " next-hop " + addr

class Cvt_RtMap_SetIPNxtHop_Del(Cvt_RtMap_SetIPNxtHop):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        # we must remove all the 'set ip next-hop' commands individually
        l = self.enter(rtmap, old, seq)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPNxtHop_Add(Cvt_RtMap_SetIPNxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(rtmap, new, seq)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(" " + self._cmd(new_nexthop))
        return l


class Cvt_RtMap_SetIPNxtHopVrfy(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop-verify-availability", None

    def _cmd(self, seq, nexthop):
        return ("set ip next-hop verify-availability %s %s track %d"
                     % (nexthop["addr"], seq, nexthop["track-obj"]))

class Cvt_RtMap_SetIPNxtHopVrfy_Del(Cvt_RtMap_SetIPNxtHopVrfy):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq, nexthop_seq):
        return self.enter(rtmap, old, seq) + [
                   " no "
                       + self._cmd(nexthop_seq,
                                   self.get_ext(old, nexthop_seq))]

class Cvt_RtMap_SetIPNxtHopVrfy_Add(Cvt_RtMap_SetIPNxtHopVrfy):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq, nexthop_seq):
        # individual entries (ordered by sequence number) can be replaced but
        # the old entry must be removed first, before the new one added
        l = self.enter(rtmap, new, seq)
        if old:
            l.append(" no "
                     + self._cmd(nexthop_seq, self.get_ext(old, nexthop_seq)))
        l.append(" " + self._cmd(nexthop_seq, self.get_ext(new, nexthop_seq)))
        return l


class Cvt_RtMap_SetIPv6NxtHop(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ipv6-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        return "set ipv6 next-hop " + addr

class Cvt_RtMap_SetIPv6NxtHop_Del(Cvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        # we must remove all the 'set ip next-hop' commands individually
        l = self.enter(rtmap, old, seq)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPv6NxtHop_Add(Cvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(rtmap, new, seq)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(" " + self._cmd(new_nexthop))
        return l


class Cvt_RtMap_SetLocalPref(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "local-preference"

class Cvt_RtMap_SetLocalPref_Del(Cvt_RtMap_SetLocalPref):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return self.enter(rtmap, old, seq) + [" no set local-preference"]

class Cvt_RtMap_SetLocalPref_Add(Cvt_RtMap_SetLocalPref):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        return self.enter(rtmap, new, seq) + [
                   " set local-preference " + str(self.get_ext(new))]


class Cvt_RtMap_SetVRF(DiffConvert_RtMap_Entry):
    # this handles both 'set global' and 'set vrf ...'
    cmd = tuple()
    ext = "set", "vrf"

    def _cmd(self, entry):
        vrf = self.get_ext(entry)
        return "set " + (("vrf " + vrf) if vrf else "global")

class Cvt_RtMap_SetVRF_Del(Cvt_RtMap_SetVRF):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return self.enter(rtmap, old, seq) + [" no " + self._cmd(old)]

class Cvt_RtMap_SetVRF_Add(Cvt_RtMap_SetVRF):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        if old:
            l.append(" no " + self._cmd(old))
        l.append(" " + self._cmd(new))
        return l



# ROUTER BGP ...



class Cvt_RtrBGP(DiffConvert):
    cmd = "router", "bgp", None

    def remove(self, old, asn):
        return "no router bgp " + str(asn)

    def add(self, new, asn):
        return "router bgp " + str(asn)


class DiffConvert_RtrBGP(DiffConvert):
    context = "router", "bgp", None

    def enter(self, asn):
        return ["router bgp " + str(asn)]


class Cvt_RtrBGP_BGPRtrID(DiffConvert_RtrBGP):
    cmd = "router-id",

    def remove(self, old, asn):
        return self.enter(asn) + [" no bgp router-id"]

    def update(self, old, upd, new, asn):
        return self.enter(asn) + [" bgp router-id " + new]


class Cvt_RtrBGP_Nbr(DiffConvert_RtrBGP):
    cmd = "neighbor", None

    def remove(self, old, *args):
        c, (nbr, ) = self._context_args(args)
        # when removing a neighbor that is a peer-group, we need to
        # state that
        return self.enter(*c) + [
                   "  no neighbor %s%s"
                       % (nbr,
                          " peer-group" if old.get("type") == "peer-group"
                              else "")]

    def add(self, new, *args):
        c, (nbr, ) = self._context_args(args)
        # we only explicitly need to add a neighbor if it's a peer-group
        # (normally, a neighbor is created implicitly by configuring
        # settings for it)
        if new.get("type") == "peer-group":
            return self.enter(*c) + ["  neighbor %s peer-group" % nbr]


class DiffConvert_RtrBGP_Nbr(DiffConvert_RtrBGP):
    context = DiffConvert_RtrBGP.context + Cvt_RtrBGP_Nbr.cmd

    # we don't want the neighbor as part of the context
    _context_args_offset = -1


class Cvt_RtrBGP_Nbr_FallOver(DiffConvert_RtrBGP_Nbr):
    cmd = "fall-over",

    def remove(self, old, asn, nbr):
        return self.enter(asn) + [" no neighbor %s fall-over"]

    def update(self, old, upd, new, asn, nbr):
        return self.enter(asn) + [
                   " neighbor %s fall-over %s"
                       % (nbr,
                          ("bfd " + new["bfd"]) if "bfd" in new
                               else "route-map " + new["route-map"])]


class Cvt_RtrBGP_Nbr_Pwd(DiffConvert_RtrBGP_Nbr):
    cmd = "password",

    def remove(self, old, asn, nbr):
        return self.enter(asn) + [" no neighbor %s password"]

    def update(self, old, upd, new, asn, nbr):
        return self.enter(asn) + [
                   " neighbor %s password encryption %d %s"
                       % (nbr, new["encyrption"], new["password"])]


class Cvt_RtrBGP_Nbr_PrGrpMbr(DiffConvert_RtrBGP_Nbr):
    # this converter is used to add or remove a neighbor to/from a
    # peer-group
    cmd = "peer-group",

    def remove(self, old, *args):
        c, (nbr, ) = self._context_args(args)
        return self.enter(*c) + [" no neighbor %s peer-group" % nbr]

    def update(self, old, upd, new, *args):
        c, (nbr, ) = self._context_args(args)
        return self.enter(*c) + [" neighbor %s peer-group %s" % (nbr, new)]


class Cvt_RtrBGP_Nbr_RemAS(DiffConvert_RtrBGP_Nbr):
    cmd = "remote-as",

    def remove(self, old, asn, nbr):
        return self.enter(asn) + [" no neighbor %s remote-as"]

    def update(self, old, upd, new, asn, nbr):
        return self.enter(asn) + [" neighbor %s remote-as %s" % (nbr, new)]


class Cvt_RtrBGP_Nbr_UpdSrc(DiffConvert_RtrBGP_Nbr):
    cmd = "update-source",

    def remove(self, old, asn, nbr):
        return self.enter(asn) + [" no neighbor %s update-source" % nbr]

    def update(self, old, upd,new, asn, nbr):
        return self.enter(asn) + [" neighbor %s update-source %s" % (nbr, new)]


# router bgp ... address-family ... [vrf ...]


# working out the address-family line is complicated and we do it in
# several places, so separate it into a function

def _RtrBGP_AF(vrf, af):
    # address families in the global routing table as in a VRF called
    # '_default' as a special case
    return (" address-family %s%s"
                % (af, (" vrf " + vrf) if vrf != "_default" else ""))


class Cvt_RtrBGP_AF(DiffConvert_RtrBGP):
    cmd = "vrf", None, "address-family", None

    def remove(self, old, asn, vrf, af):
        return self.enter(asn) + [" no" + _RtrBGP_AF(vrf, af)]

    def add(self, new, asn, vrf, af):
        return self.enter(asn) + [_RtrBGP_AF(vrf, af)]



class DiffConvert_RtrBGP_AF(DiffConvert_RtrBGP):
    context = DiffConvert_RtrBGP.context + Cvt_RtrBGP_AF.cmd

    def enter(self, asn, vrf, af):
        return super().enter(asn) + [_RtrBGP_AF(vrf, af)]


class Cvt_RtrBGP_AF_Nbr(DiffConvert_RtrBGP_AF, Cvt_RtrBGP_Nbr):
    pass


class DiffConvert_RtrBGP_AF_Nbr(DiffConvert_RtrBGP_AF):
    context = DiffConvert_RtrBGP_AF.context + Cvt_RtrBGP_AF_Nbr.cmd


class Cvt_RtrBGP_AF_Nbr_Act(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "activate",

    def remove(self, old, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + ["  no neighbor %s activate" % nbr]

    def add(self, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + ["  neighbor %s activate" % nbr]


class Cvt_RtrBGP_AF_Nbr_AddPath(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "additional-paths",

    def _add_paths(self, p):
        return (
            " ".join([a for a in [ "send", "receive", "disable" ] if a in p]))

    def remove(self, old, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s additional-paths" % nbr]

    def truncate(self, old, rem, new, asn, vrf, af, nbr):
        # we can't remove types of additional-path, only provide a
        # complete new list
        return self.update(old, None, new, asn, vrf, af, nbr)

    def update(self, old, upd, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s additional-paths %s"
                       % (nbr, self._add_paths(new))]


class Cvt_RtrBGP_AF_Nbr_AdvAddPath(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "advertise-additional-paths", None

    def remove(self, old, asn, vrf, af, nbr, adv):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s advertise additional-paths %s"
                       % (nbr, adv)]

    def update(self, old, upd, new, asn, vrf, af, nbr, adv):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s advertise additional-paths %s"
                       % (nbr, ("best %d" % new) if adv == "best" else adv)]


class Cvt_RtrBGP_AF_Nbr_FltLst(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "filter-list", None

    def remove(self, old, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s filter-list %d %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s filter-list %d %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_Nbr_PrGrpMbr(
          DiffConvert_RtrBGP_AF_Nbr, Cvt_RtrBGP_Nbr_PrGrpMbr):

    pass


class Cvt_RtrBGP_AF_Nbr_Pfx(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "prefix-list", None

    def remove(self, old, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s prefix-list %s %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s prefix-list %s %s" % (nbr, new, dir_)]


class Cvr_RtrBGP_AF_Nbr_RtMap(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "route-map", None

    def remove(self, old, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s route-map %s %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s route-map %s %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_Nbr_SndCmty(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "send-community", None

    # the 'neighbor ... send-community' command is odd in that the
    # 'standard', 'extended' and 'both' options don't replace the
    # current setting but add or remove those communities to it
    #
    # the configuration is expressed as a set containing none, one or
    # both of 'standard' and 'extended'

    def remove(self, old, asn, vrf, af, nbr, cmty):
       return self.enter(asn, vrf, af) + [
                   "  no neighbor %s send-community %s" % (nbr, cmty)]

    def update(self, old, upd, new, asn, vrf, af, nbr, cmty):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s send-community %s" % (nbr, cmty)]


class Cvt_RtrBGP_AF_Nbr_SoftRecfg(DiffConvert_RtrBGP_AF_Nbr):
    cmd = "soft-reconfiguration",

    def remove(self, old, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s soft-reconfiguration %s" % (nbr, old)]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s soft-reconfiguration %s" % (nbr, new)]


class Cvt_RtrBGP_AF_Redist(DiffConvert_RtrBGP_AF):
    cmd = "redistribute", None

    def remove(self, old, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + ["  no redistribute " + proto]

    def add(self, new, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + ["  redistribute " + proto]


class DiffConvert_RtrBGP_AF_Redist(DiffConvert_RtrBGP_AF):
    context = DiffConvert_RtrBGP_AF.context + Cvt_RtrBGP_AF_Redist.cmd


class Cvt_RtrBGP_AF_Redist_RtMap(DiffConvert_RtrBGP_AF_Redist):
    cmd = "route-map",

    def remove(self, old, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + [
                   "  no redistribute %s route-map %s" % (proto, old)]

    def update(self, old, upd, new, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + [
                   "  redistribute %s route-map %s" % (proto, new)]


class Cvt_RtrBGP_AF_Redist_Metric(DiffConvert_RtrBGP_AF_Redist):
    cmd = "metric",

    def remove(self, old, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + [
                   "  no redistribute %s metric" % proto]

    def update(self, old, upd, new, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + [
                   "  redistribute %s metric %d" % (proto, new)]



# ROUTER OSPF ...



class Cvt_RtrOSPF(DiffConvert):
    cmd = "router", "ospf", None

    def remove(self, old, proc):
        return "no router ospf " + str(proc)

    def add(self, new, proc):
        return "router ospf " + str(proc)


class DiffConvert_RtrOSPF(DiffConvert):
    context = "router", "ospf", None

    def enter(self, proc):
        return ["router ospf " + str(proc)]


class Cvt_RtrOSPF_Id(DiffConvert_RtrOSPF):
    cmd = "id",

    def remove(self, old, proc):
        return self.enter(proc) + [" no router-id"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" router-id " + new]


class Cvt_RtrOSPF_AreaNSSA(DiffConvert_RtrOSPF):
    cmd = "area", None, "nssa"

    def remove(self, old, proc, area):
        return self.enter(proc) + [" no area %s nssa" % area]

    def update(self, old, upd, new, proc, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(proc) + [" area %s nssa%s" % (area, s)]


class Cvt_RtrOSPF_PasvInt_Dflt(DiffConvert_RtrOSPF):
    cmd = "passive-interface", "default"

    def remove(self, old, proc):
        return self.enter(proc) + [
                   " %spassive-interface default" % ("no " if old else "")]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [
                   " %spassive-interface default" % ("" if new else "no ")]


class Cvt_RtrOSPF_PasvInt_Int(DiffConvert_RtrOSPF):
    cmd = "passive-interface", "interface", None

    def remove(self, old, proc, int_name):
        return self.enter(proc) + [
                   " %spassive-interface %s"
                       % ("no " if old else "", int_name)]

    def update(self, old, upd, new, proc, int_name):
        return self.enter(proc) + [
                   " %spassive-interface %s"
                       % ("" if new else "no ", int_name)]



# ROUTER OSPFV3 ...



class Cvt_RtrOSPFv3(DiffConvert):
    cmd = "router", "ospfv3", None

    def remove(self, old, proc):
        return "no router ospfv3 " + str(proc)

    def add(self, new, proc):
        return "router ospfv3 " + str(proc)


class DiffConvert_RtrOSPFv3(DiffConvert):
    context = "router", "ospfv3", None

    def enter(self, proc):
        return ["router ospfv3 " + str(proc)]


class Cvt_RtrOSPFv3_Id(DiffConvert_RtrOSPFv3):
    cmd = "id",

    def remove(self, old, proc):
        return self.enter(proc) + [" no router-id"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" router-id " + new]


class Cvt_RtrOSPFv3_AreaNSSA(DiffConvert_RtrOSPFv3):
    cmd = "area", None, "nssa"

    def remove(self, old, proc, area):
        return self.enter(proc) + [" no area %s nssa" % area]

    def update(self, old, upd, new, proc, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(proc) + [" area %s nssa%s" % (area, s)]


class Cvt_RtrOSPFv3_AF(DiffConvert_RtrOSPFv3):
    cmd = "address-family", None

    def remove(self, old, vrf, af):
        return self.enter(vrf) + [" no address-family " + af]

    def add(self, new, vrf, af):
        return self.enter(vrf) + [" address-family " + af]


class DiffConvert_RtrOSPFv3_AF(DiffConvert_RtrOSPFv3):
    context = DiffConvert_RtrOSPFv3.context + Cvt_RtrOSPFv3_AF.cmd

    def enter(self, vrf, af):
        return super().enter(vrf) + [" address-family " + af]


class Cvt_RtrOSPFv3_AF_PasvInt_Dflt(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface", "default"

    def remove(self, old, proc, af):
        return self.enter(proc, af) + [
                   " %spassive-interface default" % ("no " if old else "")]

    def update(self, old, upd, new, proc, af):
        return self.enter(proc, af) + [
                   "  %spassive-interface default" % ("" if new else "no ")]


class Cvt_RtrOSPFv3_AF_PasvInt_Int(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface", "interface", None

    def remove(self, old, proc, af, int_name):
        return self.enter(proc, af) + [
                   "  %spassive-interface %s"
                       % ("no " if old else "", int_name)]

    def update(self, old, upd, new, proc, af, int_name):
        return self.enter(proc, af) + [
                   "  %spassive-interface %s"
                       % ("" if new else "no ", int_name)]
