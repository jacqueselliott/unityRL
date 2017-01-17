using UnityEngine;
using System.Collections;
using WebSocketSharp;

public class DataTrack : MonoBehaviour {

	WebSocket ws_cur;
    GameObject drone;
    GameObject goal;
    Rigidbody droneRigidbody;
    private Vector3 droneCoords;
    private Vector3 droneVelocity;
    private Vector3 goalCoords;

    private Vector3 dir0;
    private Vector3 dir1;
    private Vector3 dir2;
    private Vector3 dir3;

    private Movement droneMovement;

    // Use this for initialization
    void Start () {
        dir0 = new Vector3(1f, 0f, 0f);
        dir1 = new Vector3(0f, 0f, 1f);
        dir2 = new Vector3(0f, 0f, -1f);
        dir3 = new Vector3(-1f, 0f, 0f);
        drone = GameObject.FindGameObjectWithTag("Drone");
        droneMovement = drone.GetComponent<Movement>();
        droneRigidbody = drone.GetComponent<Rigidbody>();
        goal = null;
		ws_cur = new WebSocket ("ws://localhost:9001");
		ws_cur.OnMessage += (sender, e) => {
			if (e.IsText) {
                if (!droneMovement.netControlled)
                {
                    droneMovement.netControlled = true;
                }
				Debug.Log(e.Data.ToString());
				//Handles received action
				int action = int.Parse(e.Data.ToString());
                if (action == 0) { droneMovement.direction = dir0; }
                else if (action == 1) { droneMovement.direction = dir1; }
                else if (action == 2) { droneMovement.direction = dir2; }
                else if (action == 3) { droneMovement.direction = dir3; }
            }
		};
		ws_cur.Connect ();
		ws_cur.Send ("unity");
	}
	
	// Update is called once per frame
	void Update () {
        if (gameObject.transform.childCount < 1)
        {
            goal = null;
        }
        if (gameObject.transform.childCount == 1 && goal == null)
        {
            goal = gameObject.transform.GetChild(0).gameObject;
        }
		if (goal != null) {
  
			goalCoords = goal.transform.position;
			droneCoords = drone.transform.position;
			droneVelocity = droneRigidbody.velocity;
			ws_cur.Send (buildOutput());
		}
	}

	string buildOutput() {
		string coord = round_dp (droneCoords.x).ToString () + ':' + round_dp (droneCoords.z).ToString () +':';
		string veloc = round_dp (droneVelocity.x).ToString () + ':' + round_dp (droneVelocity.z).ToString () +':';
		string goal = round_dp (goalCoords.x).ToString () + ':' + round_dp (goalCoords.z).ToString ();
		return coord + veloc + goal;
	}

	float round_dp(float input){
		return Mathf.Round (input * 10f) / 10f;
	}
}
