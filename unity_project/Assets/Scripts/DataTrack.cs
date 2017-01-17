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
        if (goal == null)
        {
            goalCoords = new Vector3(0f, -1000f, 0f);
        } else
        {
            goalCoords = goal.transform.position;
        }
        droneCoords = drone.transform.position;
        droneVelocity = droneRigidbody.velocity;
		ws_cur.Send(droneVelocity.ToString());
        Debug.Log(droneCoords);
        Debug.Log(droneVelocity);
        Debug.Log(goalCoords);
	}
}
