from preservationdatabase.models import CarinianaPreservation, \
    ClockssPreservation, HathiPreservation, LockssPreservation, \
    PKPPreservation, PorticoPreservation

archives = {
    'cariniana': CarinianaPreservation,
    'clockss': ClockssPreservation,
    'hathitrust': HathiPreservation,
    'lockss': LockssPreservation,
    'pkp': PKPPreservation,
    'portico': PorticoPreservation
}
