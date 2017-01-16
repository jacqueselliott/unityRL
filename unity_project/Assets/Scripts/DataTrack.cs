using UnityEngine;
using System.Collections;

public class DataTrack : MonoBehaviour {

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
        Debug.Log(droneCoords);
        Debug.Log(droneVelocity);
        Debug.Log(goalCoords);
	}
}
