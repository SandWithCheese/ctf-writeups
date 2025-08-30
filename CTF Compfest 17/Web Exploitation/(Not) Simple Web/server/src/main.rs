use hyper::service::{make_service_fn, service_fn};
use hyper::{Body, Request, Response, Server, StatusCode};
use include_dir::{Dir, include_dir};
use mime_guess;
use base64::prelude::*;
use std::env;

static STATIC_DIRECTORY: Dir = include_dir!("$CARGO_MANIFEST_DIR/src/static");

async fn handle(req: Request<Body>) -> Result<Response<Body>, hyper::Error> {
    println!("[Request]");
    println!("{:#?}", req);

    let path = req.uri().path().to_owned();
    let body_bytes = hyper::body::to_bytes(req.into_body()).await?;
    println!("[Body] {} bytes", body_bytes.len());
    if let Ok(s) = std::str::from_utf8(&body_bytes) {
        println!("{}", s);
    }

    // Normalize root to index.html
    let rel_path = if path == "/" {
        "index.html"
    } else {
        &path[1..] // strip leading slash
    };

    let file = STATIC_DIRECTORY
        .get_file(rel_path)
        .unwrap_or(STATIC_DIRECTORY.get_file("not_found.html").unwrap());

    let mime = mime_guess::from_path(rel_path).first_or_octet_stream();
    let mime_header = {
        if mime.type_() == "text" {
            format!("{}; charset=UTF-8", mime.essence_str())
        } else {
            mime.to_string()
        }
    };

    let body = if rel_path != "secret.html" {
        Body::from(file.contents())
    } else {
        let flag = env::var("FLAG").unwrap();
        Body::from(
            str::from_utf8(file.contents())
                .unwrap()
                .replace("{{ FLAG }}", &BASE64_STANDARD.encode(flag)),
        )
    };

    let status = if rel_path != "not_found.html" {
        StatusCode::OK
    } else {
        StatusCode::NOT_FOUND
    };

    Ok(Response::builder()
        .header("Content-Type", mime_header)
        .status(status)
        .body(body)
        .unwrap())
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();

    let port = args.get(1).expect("Provide port!").parse().unwrap();
    env::var("FLAG").expect("Provide FLAG env!");

    let addr = ([0, 0, 0, 0], port).into();
    let make_svc = make_service_fn(|_conn| async { Ok::<_, hyper::Error>(service_fn(handle)) });

    println!("Listening on http://{}", addr);
    Server::bind(&addr).serve(make_svc).await.unwrap();
}
