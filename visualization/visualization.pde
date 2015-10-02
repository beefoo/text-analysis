
// animation
int fps = 30;
String outputFrameFile = "output/frames/frames-#####.png";
boolean captureFrames = false;

// data
String dataFile = "../output/moby_dick/emotion.csv";
String chaptersFile = "../output/moby_dick_chapters.json";
JSONArray chaptersJSON;
String[] dataHeaders;
Table dataTable;
StringList chapters;
ArrayList<DataRow> data;
int columnCount;

// resolution
int canvasW = 1280;
int canvasH = 720;

// text
int fontSize = 28;
PFont font = createFont("OpenSans-Semibold", fontSize, true);

// layout
int padding = 80;
int labelHeight = 80;
float columnWidth = 0;
int columnHeight = canvasH - padding * 2 - labelHeight;

// colors
color bgColor = #2d2929;
color textC = #f4f3ef;

// time
float startMs = 0;
float stopMs = 120000;
float elapsedMs = startMs;
float frameMs = (1.0/fps) * 1000;
float msPerRow = 0;

void setup() {
  // set the stage
  size(canvasW, canvasH);
  colorMode(RGB, 255, 255, 255, 100);
  frameRate(fps);
  smooth();
  noStroke();
  noFill();

  // read data
  dataTable = loadTable(dataFile, "header");
  dataHeaders = dataTable.getColumnTitles();
  data = new ArrayList<DataRow>();
  for (TableRow row : dataTable.rows()) {
    data.add(new DataRow(row, dataHeaders));
  }
  columnCount = dataHeaders.length - 1;

  // read chapter data
  chaptersJSON = loadJSONArray(chaptersFile);
  chapters = new StringList();
  for (int i = 0; i < chaptersJSON.size(); i++) {
    chapters.append(chaptersJSON.getString(i));
  }

  // calculation
  msPerRow = stopMs / data.size();
  columnWidth = 1.0 * (canvasW-padding*columnCount-padding) / columnCount;

  // noLoop();
}

void draw() {
  background(bgColor);
  textFont(font);

  DataRow row = data.get(data.size()-1);
  float ms = 0;
  for (DataRow r : data) {
    if (ms >= elapsedMs) {
      row = r;
      break; 
    }
    ms += msPerRow;
  }
  
  // chapter
  textAlign(CENTER, TOP);
  text("Chapter " + (row.getChapter()+1) + ": " + chapters.get(row.getChapter()), padding, padding, canvasW-padding*2, padding);

  float x = padding;
  int text_y1 = canvasH-padding-labelHeight;
  for(int i=0; i<columnCount; i++) {

    // draw rect
    fill(#666666);
    float h = row.getValue(i) * columnHeight;
    float y = padding + (columnHeight-h);
    rect(x, y, columnWidth, h);

    // draw text
    fill(textC);
    textAlign(CENTER, BOTTOM);
    text(dataHeaders[i], x-padding, text_y1, columnWidth+padding*2, labelHeight);

    x = x + columnWidth + padding;
  }
  
  // increment time
  elapsedMs += frameMs;
}

void mousePressed() {
  // saveFrame("output/frame.png");
  exit();
}

class DataRow
{
  FloatList myData;
  int chapter;

  DataRow(TableRow _row, String[] _headers) {
    myData = new FloatList();

    for(int i=0; i<_headers.length-1; i++) {
      myData.append(_row.getFloat(_headers[i]));
    }

    chapter = _row.getInt("chapter");
  }
  
  int getChapter() {
    return chapter; 
  }

  float getValue(int column) {
    return myData.get(column);
  }
}
