# CCS Deployment Simulation
Modeling CCS deployment strategies for Net Zero California

Three scenarios:
1. Coordinated
   - One party builds out the transport + storage grid
   - Individual capture projects link into the central grid infrastructure
   - Coordination problem is resolved through guaranteed transport + storage infrastructure
2. Multi-party uncoordinated
   - Each CCS project involves two parties: capture and transport + storage 
   - Interdependencies between investment stages of two parties may lead to cascading delays and project abandonment
   - Coordination problem
3. Independent uncoordinated
   - One party builds all components of the CCS project (capture, transport, and storage)
   - No coordination problem, but limits pool of actors to those with expertise/ resources across all stages of the chain

Model architecture:
- Game-theoretic component: coordination problem
- DAG: time-based sequencing and coordination 
