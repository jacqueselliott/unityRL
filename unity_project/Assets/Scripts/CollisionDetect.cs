using UnityEngine;
using System.Collections;

public class CollisionDetect : MonoBehaviour {

    private GameObject controller;

    private DataTrack dataScript;

	public bool dest = false;

	// Use this for initialization
	void Start () {
        controller = GameObject.FindGameObjectWithTag("Controller");
        dataScript = controller.GetComponent<DataTrack>();
	}
	
	// Update is called once per frame
	void Update () {
		if (dest) {
			Destroy (gameObject);
			dest = false;
		}
	}
    void OnCollisionEnter(Collision other)
    {
        if(other.gameObject.tag == "Drone")
        {
            Destroy(gameObject);
            dataScript.success = 1;

        }
    }
}
