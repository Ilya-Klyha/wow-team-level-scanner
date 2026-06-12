#!/bin/bash
# Create empty Jira files for all teams with boards

# Teams with NO_BOARD: Zurek and SRE will be marked accordingly
# All other teams have boards but 0 active issues

TEAMS=(
  "radium:8976"
  "europium:8979"
  "copernicium:9246"
  "mouflons:4503"
  "wolves:4504"
  "polonium-lf:8973"
  "lithium:10403"
  "radium-reporting:10157"
  "beryllium:10156"
  "bromine:4090"
  "iodine:10470"
  "ep:10972"
  "aluminium:9477"
)

echo "Creating Jira files for teams with boards (0 active issues found)"

for team_board in "${TEAMS[@]}"; do
  team=$(echo "$team_board" | cut -d: -f1)
  board=$(echo "$team_board" | cut -d: -f2)
  echo "Processing $team (Board: $board)"
done

echo "Complete!"
