# Carbon Capture and Storage Deployment Simulation
A simulation framework for Carbon Capture and Storage (CCS) deployment. Developed to evaluate policy options for Net Zero California's bid to operationalize 100 million Mt/yr of carbon capture by 2024. This framework is an adaptation of the CADENCE model developed by Claire Goldberg

## World 1: Coordinated
- Transport and storage infrastructure proceed with backing (their investment decisions are not impacted by wait-time)
- Coordination problem is partly resolved through guaranteed payout for transport and storage infrastructure
  
### Scenario 1: Incentive-Driven Rush
- Projects can begin definition once their predecessors have been commissioned
- No phase enforcement 

### Scenario 2: Infrastructure Build-Out
- Enforcement of a front-loaded transport and storage build-out
- Capture projects begin definition when transport and storage build-out meets threshold

## World 2: Uncoordinated
- Each CCS project involves three: capture, transport, and storage
- Interdependencies between investment stages of two parties may lead to cascading delays and project abandonment
- Game-theoretic simulation of the coordination problem (stag hunt) by setting abandonment probability as a function of partner-wait time

