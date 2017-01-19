using UnityEngine;
using System.Collections;

public class Movement : MonoBehaviour {

    private Rigidbody droneRigidbody;
    public float forceMagnitude;
    public float discreteMagnitude;
    public Vector3 direction;
    public bool netControlled = false;
    private Vector3 newDirection;
    private Vector3 targetPosition;
    public bool toSend = false;
    private DataTrack dataTrackScript;

    private float groundSize;

    public bool discrete;

    private bool keyDown;

	// Use this for initialization
	void Start () {
        droneRigidbody = gameObject.GetComponent<Rigidbody>();
        GameObject ground = GameObject.Find("Ground");
        dataTrackScript = GameObject.FindGameObjectWithTag("Controller").GetComponent<DataTrack>();
        groundSize = ground.GetComponent<Collider>().bounds.size.x;
        Respawn();
	}

    private void Respawn()
    {
        //ensures spawning in grid
        float offset = 0.5f % discreteMagnitude;
        transform.position = new Vector3(offset, 0.5f, offset);
    }

    // Update is called once per frame
    void Update()
    {
        if (!netControlled)
        {
            direction = Vector3.zero;
            direction = CreateDirectionFromInput();
        }
        else
        {
            if (direction != Vector3.zero)
            {
                toSend = true;
            }
        }
        if (discrete)
        {
            MoveDiscretely();
        }
        else
        {
            ApplyForce();
        }
        transform.position = new Vector3(transform.position.x, 0.5f, transform.position.z);
    }

    void LateUpdate()
    {
        if (discrete)
        {
            transform.position = targetPosition;
        }
        if (netControlled && toSend)
        {
            dataTrackScript.SendData();
            direction = Vector3.zero;
            toSend = false;
        }

    }

    private Vector3 CreateDirectionFromInput()
    {
        if (discrete)
        {
            direction = DiscreteDirection();
        }
        else
        {
            direction = ContinuousDirection();
        }
        return direction;
    }

    private Vector3 ContinuousDirection()
    {
        float inx = Input.GetAxis("Horizontal");
        float inz = Input.GetAxis("Vertical");
        direction = new Vector3(inx, 0, inz);
        return direction;
    }

    private Vector3 DiscreteDirection()
    {
        if (Input.GetKeyDown("w"))
        {
            direction = new Vector3(0f, 0f, 1f);
        }
        if (Input.GetKeyDown("a"))
        {
            direction = new Vector3(-1f, 0f, 0f);
        }
        if (Input.GetKeyDown("s"))
        {
            direction = new Vector3(0f, 0f, -1f);
        }
        if (Input.GetKeyDown("d"))
        {
            direction = new Vector3(1f, 0f, 0f);
        }
        return direction;
    }

    private void ApplyForce()
    {
        newDirection = direction * forceMagnitude;
        droneRigidbody.AddForce(newDirection);
        // fix roll and pitch
        transform.eulerAngles = new Vector3(0f, transform.eulerAngles.y, 0f);
    }

    private void MoveDiscretely()
    {
        newDirection = direction * discreteMagnitude;
        bool outside = CheckOutside(transform.position + newDirection);
        if (!outside)
        {
            targetPosition = transform.position + newDirection;
            transform.position += newDirection;
        }
        //fix roll, pitch, yaw
        transform.eulerAngles = new Vector3(0f, 0f, 0f);
    }

    private bool CheckOutside(Vector3 newPosition)
    {
        float edgeDistance = groundSize / 2;
        float x = newPosition.x;
        float z = newPosition.z;
        if (Mathf.Abs(x) > edgeDistance) { return true; }
        if (Mathf.Abs(z) > edgeDistance) { return true; }
        return false;
    }
}
