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

	// Use this for initialization
	void Start () {
        drone = GameObject.FindGameObjectWithTag("Drone");
        droneRigidbody = drone.GetComponent<Rigidbody>();
        goal = null;
		ws_cur = new WebSocket ("ws://localhost:9001");
		ws_cur.OnMessage += (sender, e) => {
			if (e.IsText) {
				Debug.Log(e.ToString());
				//Handles received action
				int action = int.Parse(e.ToString());
			}
		};
		ws_cur.Connect ();
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
