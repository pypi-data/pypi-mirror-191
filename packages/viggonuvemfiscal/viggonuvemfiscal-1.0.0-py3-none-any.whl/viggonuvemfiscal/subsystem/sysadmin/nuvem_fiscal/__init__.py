from viggocore.common import subsystem
from viggonuvemfiscal.subsystem.sysadmin.nuvem_fiscal \
  import resource, manager

subsystem = subsystem.Subsystem(resource=resource.NuvemFiscal,
                                manager=manager.Manager)
