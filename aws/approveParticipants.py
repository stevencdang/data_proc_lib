import mongohq
import mturk

priming_exp = {'desc': "rare vs common individual brainstorming",
                "hit_id": '3ZURAPD288NJZ4HUTVEJXT1RKF51F5'
              }


if __name__ == '__main__':
  params = mongohq.ideagenstest 
  db = mongohq.get_mongodb(params['url'],
                   params['port'],
                   params['dbName'], 
                   params['user'],
                   params['pswd'])


  m = mturk.MechanicalTurk()
  # Confirms Mturk connection is valid
  r = m.request("GetAccountBalance")
  if r.valid:
      print r.get_response_element("AvailableBalance")

  # Get all submitted assignments for the hit
  r = m.request("GetAssignmentsForHIT",
      {"HITId": priming_exp["hit_id"]}
      )

  if r.valid:
      print r.get_response_element("assignment")
  else:
      print "failed"
