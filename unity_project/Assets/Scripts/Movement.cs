using UnityEngine;
using System.Collections;

public class Movement : MonoBehaviour {

    private Rigidbody droneRigidbody;
    public float forceMagnitude = 0;
    public Vector3 direction;
    public bool netControlled = false;
    private Vector3 newDirection;

	// Use this for initialization
	void Start () {
        droneRigidbody = gameObject.GetComponent<Rigidbody>();
	}
	
	// Update is called once per frame
	void Update () {
        if (!netControlled)
        {
            float inx = Input.GetAxis("Horizontal");
            float inz = Input.GetAxis("Vertical");
            direction = new Vector3(inx, 0, inz);
        }
        newDirection = direction*forceMagnitude;
        droneRigidbody.AddForce(newDirection);
        transform.position = new Vector3(transform.position.x, 0.5f, transform.position.z);
        transform.eulerAngles = new Vector3(0f, transform.eulerAngles.y, 0f);
	}
}
